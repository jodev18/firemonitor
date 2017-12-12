<?php

require('../controller/connect_env.php');

ini_set('display_errors', 'on');

if(isset($_POST)){

	$thres_temp = $_POST['temp_set'];
	$thres_humd = $_POST['humidity_set'];

	if(isset($thres_temp)){
		if(isset($thres_humd)){
			$sql = "INSERT INTO tbl_threshold(thres_temp,thres_humidity) VALUES (?,?);";
			
			$prep = $conn_env->prepare($sql);
			
			$prep->bind_param("ii",$thres_temp,$thres_humd);

			if($prep->execute()){
				echo '<script> alert("Threshold successfully set!");
					window.location.href = "../dashboard.php"; </script>';
			}
			else{
				echo '<script> alert("Threshold failed to save!");
					window.location.href = "../dashboard.php"; </script>';
			}
			

		}
		else{
			echo '<script> alert("Please enter humidity value.");
					window.location.href = "../dashboard.php"; </script>';
		}
	}
	else{
		echo '<script> alert("Please enter temperature value.");
					window.location.href = "../dashboard.php"; </script>';
	}	




}






?>