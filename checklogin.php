<?php
  switch($_SERVER['REQUEST_METHOD']) {
      case 'POST':
        $username = $_POST['username'];
        $password = $_POST['password'];
        $command = "python /var/www/CheckLogin.py " . $username . ' ' . $password; 
        $f = popen($command, 'r');
        $return = fgets($f);
        fclose($f);
        $mysqli = mysqli_connect("localhost", "webuser", "", "mybamachecker");
        if (mysqli_connect_errno($mysqli)) {
            error_log("Failed to connect to MySQL: " . mysqli_connect_error());
            exit;
        }
        // check if the account exists
        $exists = $mysqli->query("SELECT * FROM accounts WHERE username='" 
                                 . $username . "';"); 
        if ($exists->num_rows === 0) {
            // create a new account
            $adduser = $mysqli->query("INSERT INTO accounts VALUES(UUID(), '" 
                                      . $username . "', '" 
                                      . $password . "', " 
                                      . $return[0] . ");");
            echo json_encode("Account created successfully.");
        } else {
            $userid = $exists->fetch_array()['user_id'];
            $acctpasswd = $exists->fetch_array()['password'];
            if ($acctpasswd !== $password) {
                if ($return[0] === "0") {
                    echo json_encode("Incorrect password entered.");
                    exit;
                } else {
                    $changepass = $mysqli->query("UPDATE accounts SET password='"
                                                 . $password 
                                                 . "', valid_credentials=1 WHERE user_id='"
                                                 . $userid . "';"); 
                }
            }
            $storedclasses = $mysqli->query("SELECT * FROM sections WHERE for_user_id='" 
                                            . $userid . "';");
            echo json_encode($storedclasses->fetch_array());
        }
        break;
   };        
?>
