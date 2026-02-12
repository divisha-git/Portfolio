# EmailJS Setup Instructions

## Step 1: Create EmailJS Account
1. Go to https://www.emailjs.com/
2. Sign up for a free account (allows 200 emails/month)
3. Verify your email address

## Step 2: Create Email Service
1. In EmailJS dashboard, go to "Email Services"
2. Click "Add New Service"
3. Choose "Gmail" (recommended)
4. Connect your Gmail account (mdivisha2005@gmail.com)
5. Note down the **Service ID** (e.g., "service_abc123")

## Step 3: Create Email Template
1. Go to "Email Templates"
2. Click "Create New Template"
3. Use this template content:

**Subject:** New Portfolio Contact: {{subject}}

**Body:**
```
Hello Divisha,

You have received a new message from your portfolio website:

Name: {{from_name}}
Email: {{from_email}}
Subject: {{subject}}

Message:
{{message}}

---
This message was sent from your portfolio contact form.
```

4. Note down the **Template ID** (e.g., "template_xyz789")

## Step 4: Get Public Key
1. Go to "Account" → "General"
2. Copy your **Public Key** (e.g., "user_abc123xyz")

## Step 5: Update Your Website
Replace these values in your index.html:
- `YOUR_PUBLIC_KEY` → Your actual public key
- `YOUR_SERVICE_ID` → Your service ID  
- `YOUR_TEMPLATE_ID` → Your template ID

## Example:
```javascript
emailjs.init("user_abc123xyz");
emailjs.send('service_abc123', 'template_xyz789', templateParams)
```

That's it! Your contact form will now send emails directly to your Gmail inbox.
