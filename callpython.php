<?php
  switch($_SERVER['REQUEST_METHOD']) {
      case 'POST':
        $command = "python /var/www/GetSectionAvail.py " . 
                   $_POST['username'] . ' ' . $_POST['password'] . " \"" . 
                   $_POST['term'] . "\" \"" . $_POST['subject'] . "\" \"" . 
                   $_POST['course'] . "\" \"" . $_POST['section'] . "\"";
        exec($command, $return);
        error_log($command);
        echo json_encode($return);
        break;
   };        
?>
