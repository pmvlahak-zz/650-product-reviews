<?php
if($_SERVER['REQUEST_METHOD'] === 'POST') 
{

	function debug_to_console( $input ) {

	    if ( is_array( $input ) )
	        $output = "<script>console.log( 'Debug Objects: " . implode( ',', $input) . "' );</script>";
	    else
	        $output = "<script>console.log( 'Debug Objects: " . $input . "' );</script>";
	    echo $output;
	}

	// check that form was submitted
	if( !empty( $_POST ) ){

	// remove html tags from submission (since you don't want them)
	$title = strip_tags( $_POST['review_title'] );
	$text = strip_tags( $_POST['review_text'] );
	$category = strip_tags( $_POST['category'] );
	$date = strip_tags( $_POST['date'] );
	$date_weight = strip_tags( $_POST['date_weight'] );
	$category_weight = strip_tags( $_POST['category_weight'] );
	$title_weight = strip_tags( $_POST['title_weight'] );
	$max_stars = strip_tags( $_POST['max_stars'] );


	// create an array to hold the review form info
	$record = array( 
		"title" => $title,
		"text" => $text,
		"category" => $category,
		"date" => $date,
		"date_weight" => $date_weight,
		"category_weight" => $category_weight,
		"title_weight" => $title_weight,
		"max_stars" => $max_stars
		);

	// save the review record to a .txt file for web_classifier.py
	$json = json_encode( $record );
	$fp = fopen('input.json', 'w');
	fwrite($fp, json_encode($record));
	fclose($fp);
	debug_to_console($json);
	}

	sleep(2);

	// $command = 'python test.py';
	// exec($command, $output, $status);
	// $console = "<script>console.log( 'Python command: " . $command . "' );</script>";
	// echo $console;
	// $console1 = "<script>console.log( 'Python out: " . $output . "' );</script>";
	// echo $console1;
	// $console2= "<script>console.log( 'Python status: " . $status . "' );</script>";
	// echo $console2;

	// $stars = (array) json_decode($output[0]);
	// $score = $stars['score'];
	// echo $score;
	// $arr_dump = "<script>console.log( ". $score ." );</script>";
	// echo $arr_dump;

} else { 

	// call web_classifier.py to classify the review input
	error_reporting(0);
	$command = 'python test.py';
	exec($command, $output, $status);
	$stars = (array) json_decode($output[0]);
	$score = $stars['score'];
	echo $score;
}
?>







