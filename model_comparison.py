import json
import time

def compare_models(def_text, models=['anthropic.claude-v2','anthropic-instant-v1']):
  results = {}

  for model in models:
    start_time = time.time()    
    
    # Process with current model
    response = bedrock_invoke_model(
      model_id=model,
      body=json.dumps({
        "prompt": "Extract key information from this document: " + document_text,
        "temperature": 0.0,
        "max_tokens_to_sample": 1000
      })
    )

    # Calculate metrics
    elapsed_time = time.time() - start_time
    response_body = json.loads(response['body'].read())
    output

    results[model] = {
      "time_seconds": elapsed_time,
      "output_length": len(output),
      "output_sample": output[:100] + "..."
    }

  return results