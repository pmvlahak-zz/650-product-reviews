<?php

function debug_to_console( $input ) {

    if ( is_array( $input ) )
        $output = "<script>console.log( 'Debug Objects: " . implode( ',', $input) . "' );</script>";
    else
        $output = "<script>console.log( 'Debug Objects: " . $input . "' );</script>";
    echo $output;
}

// $poster = $_POST;
// debug_to_console($poster);

// check that form was submitted
if( !empty( $_POST ) ){

// remove html tags from submission (since you don't want them)
$title = "title: ".strip_tags( $_POST['review_title'] );
$text = "text: ".strip_tags( $_POST['review_text'] );
$category = "category: ".strip_tags( $_POST['category'] );
$date = "date: ".strip_tags( $_POST['date'] );
$date_weight = "date_weight: ".strip_tags( $_POST['date_weight'] );
$category_weight = "category_weight: ".strip_tags( $_POST['category_weight'] );
$title_weight = "title_weight: ".strip_tags( $_POST['title_weight'] );


// create an array that holds your info
$record = array( $title,$text,$category,$date,$date_weight,$category_weight,$title_weight );

// save the record to your .txt file (I still recommend JSON)
$json = json_encode( $record );
$fp = fopen('review.json', 'w');
fwrite($fp, json_encode($record));
fclose($fp);

debug_to_console($json);

}

?>