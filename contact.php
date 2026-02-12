<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = htmlspecialchars(trim($_POST['name']));
    $email = htmlspecialchars(trim($_POST['email']));
    $subject = htmlspecialchars(trim($_POST['subject']));
    $message = htmlspecialchars(trim($_POST['message']));
    
    // Validation
    $errors = [];
    
    if (empty($name)) {
        $errors[] = "Name is required";
    }
    
    if (empty($email)) {
        $errors[] = "Email is required";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Invalid email format";
    }
    
    if (empty($subject)) {
        $errors[] = "Subject is required";
    }
    
    if (empty($message)) {
        $errors[] = "Message is required";
    }
    
    // If no errors, send email
    if (empty($errors)) {
        $to = "mdivisha2005@gmail.com";
        $email_subject = "Portfolio Contact: " . $subject;
        
        $email_body = "You have received a new message from your portfolio contact form.\n\n";
        $email_body .= "Name: " . $name . "\n";
        $email_body .= "Email: " . $email . "\n";
        $email_body .= "Subject: " . $subject . "\n\n";
        $email_body .= "Message:\n" . $message . "\n";
        
        $headers = "From: " . $email . "\r\n";
        $headers .= "Reply-To: " . $email . "\r\n";
        $headers .= "X-Mailer: PHP/" . phpversion();
        
        if (mail($to, $email_subject, $email_body, $headers)) {
            $success = "Thank you! Your message has been sent successfully.";
        } else {
            $error = "Sorry, there was an error sending your message. Please try again.";
        }
    } else {
        $error = implode("<br>", $errors);
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form Response</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: #121212;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .message-container {
            background: #1e1e1e;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            max-width: 500px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
        }
        .success {
            color: #4ade80;
        }
        .error {
            color: #f87171;
        }
        .back-btn {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.75rem 1.5rem;
            background: #4a9bff;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: background 0.3s;
        }
        .back-btn:hover {
            background: #6eb0ff;
        }
    </style>
</head>
<body>
    <div class="message-container">
        <?php if (isset($success)): ?>
            <h2 class="success">✓ Success!</h2>
            <p><?php echo $success; ?></p>
        <?php elseif (isset($error)): ?>
            <h2 class="error">✗ Error</h2>
            <p><?php echo $error; ?></p>
        <?php endif; ?>
        
        <a href="index.html" class="back-btn">← Back to Portfolio</a>
    </div>
</body>
</html>
