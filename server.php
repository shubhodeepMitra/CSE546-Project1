<?php
// // Specify the directory where you want to store the uploaded files.
$target_dir = "uploads/";

// // Get the file name and append it to the target directory.
$target_file = $target_dir . basename($_FILES["file"]["name"]);

// // Move the uploaded file to the target directory.
move_uploaded_file($_FILES["file"]["tmp_name"], $target_file);

$image_url = "http://<your_flask_server_ip>:<your_flask_server_port>/image"; // Replace with your Flask server IP and port.
$image_path = realpath($target_file);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $image_url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, array('file' => new CURLFILE($image_path)));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$result = curl_exec($ch);
curl_close($ch);
?>
