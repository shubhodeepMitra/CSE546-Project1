<?php
// // php -S 127.0.0.1:8000
// check if an image file was uploaded
if (isset($_FILES['myfile'])) {
    
    // // set the target URL of the Flask program
    // $url = "http://100.25.166.125:8080/image";
    
    // // prepare the image file to be sent to the Flask program
    // $file = $_FILES['myfile'];
    // $filename = $file['name'];
    // $filedata = file_get_contents('/Users/shubhodeepmitra/Downloads/imagenet-100/' . basename($_FILES["file"]["name"]));
    // $filesize = $file['size'];
    

    $target_dir = "/Users/shubhodeepmitra/Downloads/";

    // // Get the file name and append it to the target directory.
    $target_file = $target_dir . basename($_FILES["myfile"]["name"]);
    echo $_FILES["myfile"]["name"];
    
    // // Move the uploaded file to the target directory.
    move_uploaded_file($_FILES["myfile"]["tmp_name"], $target_file);
    
    $image_url = "http://100.25.166.125:8080/image"; // Replace with your Flask server IP and port.
    $image_path = realpath($target_file);


    // // set the POST request headers
    // $headers = array('Content-Type: multipart/form-data');
    
    // // set the POST request payload with the image file
    // $payload = array(
    //     'myfile' => new CURLFile($file['tmp_name'], $file['type'], $filename)
    // );
    
    // send the POST request to the Flask program
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $image_url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, array('file' => new CURLFILE($image_path)));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $result = curl_exec($ch);
    curl_close($ch);
    
    // print the result from the Flask program
    echo $result;
    
} else {
    
    // print an error message if no image file was uploaded
    echo 'Error: no image file uploaded';
    
}
?>