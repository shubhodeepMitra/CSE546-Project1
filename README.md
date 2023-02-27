# Project1
This is a project README file. This application includes a web tier, an app tier, and a PHP backend server. 

## Contributors

* Ashwin Nair
* Shubhodeep Mitra
* Raghav Aggarwal

## Member Tasks

* Ashwin Nair:
  * Worked on getting app tier code working on a startup of EC2 instance: that is for each new instance created by autoscaling functionality, the app_tier.py is run on boot and listens for messages in the SQS queue.
  * Tried many different alternatives such as trying to use the python-systemd library and modifying init.d as well. Finally got it to work by creating a cron entry using crontab and making a new AMI with the app_tier.py script and settings.yaml files included.

* Shubhodeep Mitra:
  * Developed the web_tier code for:
    * Read the Post request from the PHP server
    * Upload the image to the input S3 bucket
    * Send message request to the SQS queue
    * Implement the multi-threading version to handle multi_workload generator
  * Developed app_tier code:
    * Read from the request SQS queue.
    * Download the image based on the request message key from S3 bucket
    * Call the image classifier and read the result
    * Upload the result to the S3 output bucket
    * Send a message in the response SQS queue with the results
  * Testing of web_tier and app_tier functionality with:
    * single_workload
    * multi_workload
    * multi_workload with Auto-scaling enabled
  * Manually verifying the SQS queues and S3 buckets have the intended value.

* Raghav Aggarwal:
  * Developed the PHP backend server that acts as an interface which gets request from the workload generator and redirects the data to web_tier. 
  * Developed the code for the web_tier to listen to the response Queue and print the result (output message). 
  * Researched methods for implementing Autoscaling. Which is implemented using AWS CloudWatch alarm which is configured to automatically increase or decrease the number of EC2 instances based on the size of the SQS queue.
  * Created project Report
  
  ## To Run Application

To run this code, you should execute "tmux attach -t mytestapp" to create a new terminal window and then run "python web_tier" in that window. You will also need to customize the code to match the specifics of your S3 buckets, SQS queue, and app tier endpoint.
