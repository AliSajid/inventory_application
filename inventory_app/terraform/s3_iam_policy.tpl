{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:ListBuckets",
        "s3:HeadObject",
        "s3:GetBucketLocation",
        "s3:GetObjectVersion",
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:GetLifecycleConfiguration",
        "s3:PutLifecycleConfiguration",
        "s3:DeleteObject"
      ],
      "Resource": [
        "${bucket_arn}",
        "${bucket_arn}/*"
      ]
    }
  ]
}
