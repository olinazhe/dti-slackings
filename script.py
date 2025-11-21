import json
import sys

def filter_json_fields(input_file, output_file):
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Filter each message to keep only specified fields
    filtered_data = []
    for message in data:
        filtered_message = {
            "user": message.get("user"),
            "type": message.get("type"),
            "text": message.get("text"),
            "user_profile": {
                "display_name": message.get("user_profile", {}).get("display_name")
            },
            "reactions": []
        }
        
        # Filter reactions if they exist
        if "reactions" in message:
            for reaction in message["reactions"]:
                filtered_reaction = {
                    "name": reaction.get("name"),
                    "users": reaction.get("users"),
                    "count": reaction.get("count")
                }
                filtered_message["reactions"].append(filtered_reaction)
        
        filtered_data.append(filtered_message)
    
    # Write the filtered data to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)
    
    print(f"✓ Filtered data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python filter_json.py <input_file> [output_file]")
        print("Example: python filter_json.py data.json")
        print("Example: python filter_json.py data.json filtered_data.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # If output file not specified, create one based on input filename
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        # Add '_filtered' before the extension
        if '.' in input_file:
            name, ext = input_file.rsplit('.', 1)
            output_file = f"{name}_filtered.{ext}"
        else:
            output_file = f"{input_file}_filtered"
    
    filter_json_fields(input_file, output_file)