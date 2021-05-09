# Secret Credentials used for various tasks

secret_key = "yoursecretkey"

Email_ID = "your_email@gmail.com"
Email_pass = "yourpassword"

Email_subject = "Confirm your email for Green Division, DIU ACM"

Forget_subject = "Reset Password"

Forget_body = "You've requested to reset your password. Please visit the link below to reset your password.\n"

ignore_message= "\n\nIf you didn't send the request, ignore this mail.\n"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# Cloudinary Secrets
CLOUDINARY_CLOUD_NAME = 'cloud name of cloudinary'
CLOUDINARY_API_KEY = 'cloud api key'
CLOUDINARY_API_SECRET = 'api secret'