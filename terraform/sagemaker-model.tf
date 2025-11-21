locals {
    images = {
        cpu = "763104351884.dkr.ecr.${var.region}.amazonaws.com/huggingface-pytorch-inference:2.6.0-transformers4.49.0-cpu-py312-ubuntu22.04"
        gpu = "763104351884.dkr.ecr.${var.region}.amazonaws.com/huggingface-pytorch-inference:2.6.0-transformers4.49.0-gpu-py312-cu124-ubuntu22.04"
    }
    model_definition = {
        # By specifying anything that can change in model definition, we can get a hash so that a blue-green deployment is possible with
        # unique names on the endpoint configuration and the model
        primary_container = {
            image          = var.whisper_endpoint_gpu ? local.images["gpu"] : local.images["cpu"]
            mode           = "SingleModel"
            model_data_url = "s3://${aws_s3_object.whisper_model.bucket}/${aws_s3_object.whisper_model.key}"

            environment = {
                SAGEMAKER_REGION              = var.region
                SAGEMAKER_CONTAINER_LOG_LEVEL = 20
            }
        }
        production_variants = {
            variant_name           = "AllTraffic"
            initial_instance_count = 1
            initial_variant_weight = 1
            instance_type          = var.whisper_endpoint_gpu ? "ml.p3.2xlarge" : "ml.m5.xlarge"
        }
        model_etag      = data.archive_file.sagemaker_whisper_model.output_md5
        manual_rotation = 0  # This could be manually increased to resolve any issues with same-names
    }
}

data "archive_file" "sagemaker_whisper_model" {
  type        = "tar.gz"
  source {
    content  = file("../src/inference.py")
    filename = "code/inference.py"  # Must be in code folder for inference script to be used
  }
  output_path = "../dist/whisper_inference.tar.gz"
}

resource "aws_s3_bucket" "model" {
  bucket        = "${var.project}-model"
  force_destroy = true
}

resource "aws_s3_object" "whisper_model" {
    bucket = aws_s3_bucket.model.bucket
    key    = "custom_inference/whisper/model.tar.gz"
    source = data.archive_file.sagemaker_whisper_model.output_path
    etag   = data.archive_file.sagemaker_whisper_model.output_md5
}

data "aws_iam_policy_document" "assume_role_sagemaker" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "sagemaker_execution" {
  name               = "${var.project}-sagemaker_execution"
  assume_role_policy = data.aws_iam_policy_document.assume_role_sagemaker.json
}

data "aws_iam_policy" "sagemaker_execution_sagemaker_full_access" {
  arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}

data "aws_iam_policy" "sagemaker_execution_s3_full_access" {
  arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "sagemaker_execution_sagemaker_full_access" {
  role       = aws_iam_role.sagemaker_execution.name
  policy_arn = data.aws_iam_policy.sagemaker_execution_sagemaker_full_access.arn
}

resource "aws_iam_role_policy_attachment" "sagemaker_execution_s3_full_access" {
  role       = aws_iam_role.sagemaker_execution.name
  policy_arn = data.aws_iam_policy.sagemaker_execution_s3_full_access.arn
}

resource "aws_sagemaker_model" "whisper" {
  name               = "${var.project}-whisper"
  execution_role_arn = aws_iam_role.sagemaker_execution.arn

  primary_container {
    image          = local.model_definition.primary_container.image
    mode           = local.model_definition.primary_container.mode
    model_data_url = local.model_definition.primary_container.model_data_url
    environment    = local.model_definition.primary_container.environment
  }
}

resource "aws_sagemaker_endpoint_configuration" "whisper" {
  name = "${var.project}-whisper"

  production_variants {
    variant_name           = local.model_definition.production_variants.variant_name
    model_name             = aws_sagemaker_model.whisper.name
    initial_instance_count = local.model_definition.production_variants.initial_instance_count
    instance_type          = local.model_definition.production_variants.instance_type
    initial_variant_weight = local.model_definition.production_variants.initial_variant_weight
  }
}

resource "aws_sagemaker_endpoint" "whisper" {
  name                 = "${var.project}-whisper"
  endpoint_config_name = aws_sagemaker_endpoint_configuration.whisper.name
}
