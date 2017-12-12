<?php
//error_reporting(E_ALL ^ E_NOTICE);
//error_reporting(E_ALL ^ E_DEPRECATED);
$server = "localhost";
$username = "root";
$pass = "firemonitor";
$dbname = "firemonitor";

ini_set('display_errors', 'on');

//create connection

$conn_env = mysqli_connect($server,$username,$pass,$dbname);
//$con = mysql_connect($server,$username,$pass,$dbname);
//check conncetion

if($conn_env->connect_error){

	die ("Connection Failed! -- Environmental Data". $conn->connect_error);
}

/*
if(!$con){

	die ("Connection Failed!". mysql_error());
}

mysql_select_db("$dbname");

*/

?>