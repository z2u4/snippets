extern crate mini_v8;

use mini_v8::{MiniV8, Value};
use std::{fs};

fn main() {
    let query = "
        person.city === 'New York' && person.age > 30
    ";
    // Read JSON data 
    let json_data = fs::read_to_string("data.json")
        .map_err(|e| format!("Failed to read JSON file: {}", e));

    match parse_json(&json_data.unwrap(), query, "people", "person") {
        Ok(result) => println!("{}", result),
        Err(e) => eprintln!("Error: {}", e),
    }
}

fn parse_json(json_data: &str, raw_query: &str, dataset_name: &str, unit_name: &str) -> Result<String, String> {
    let mv8 = MiniV8::new();
    
    // Load JSON data 
    let js_script: &str = &format!("const {} = {};", dataset_name, json_data);
    
    let _ = mv8.eval::<_, Value>(js_script)
        .map_err(|e| format!("Failed to load JSON data into JavaScript environment: {}", e));

    // Parse query
    let js_query = format!("JSON.stringify({}.filter({} => {}))", dataset_name, unit_name, raw_query);


    // Execute 
    mv8.eval(js_query)  
        .map_err(|e| format!("Failed to execute query: {}", e))
}