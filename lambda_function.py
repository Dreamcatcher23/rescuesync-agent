import json
import boto3
import time
from datetime import datetime

# Initialize Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# OPTION A: Simulated Agent Memory (in production, use DynamoDB)
INCIDENT_LOG = []

def lambda_handler(event, context):
    try:
        # OPTION B: Performance tracking starts
        start_time = time.time()
        
        # Parse input
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        scenario = body.get('scenario', 'No scenario provided')
        scenario_type = body.get('scenario_type', 'building_collapse')  # OPTION C
        
        print(f"🚨 RescueSync Agent Starting - Scenario Type: {scenario_type}")
        print("🤖 Invoking Claude 3.5 Sonnet via Bedrock inference profile...")
        
        # OPTION C: Customize prompt based on scenario type
        if scenario_type == 'earthquake':
            scenario_context = """You are coordinating an EARTHQUAKE disaster response.
Consider: aftershock risks, structural instability, widespread damage, potential gas leaks."""
        elif scenario_type == 'flood':
            scenario_context = """You are coordinating a FLOOD disaster response.
Consider: water levels, drowning risks, contamination, evacuation routes."""
        else:  # building_collapse (default)
            scenario_context = """You are coordinating a BUILDING COLLAPSE disaster response.
Consider: structural integrity, trapped victims, collapse progression."""
        
        # Enhanced prompt with scenario-specific context
        prompt = f"""You are RescueSync, an advanced AI disaster response coordinator with multi-step reasoning.

{scenario_context}

SCENARIO:
{scenario}

INSTRUCTIONS:
Analyze this disaster scenario using a systematic 3-step coordination process:

STEP 1️⃣ - SEARCH PRIORITY ANALYSIS
Evaluate and rank all zones by:
- Estimated survivor count (highest priority)
- Structural safety percentage (0-100%)
- Access difficulty (Easy/Medium/Hard)

Output format:
Priority 1: [Zone] - [Survivors] people, [Safety]% safe, [Access] access
Priority 2: [Zone] - [Survivors] people, [Safety]% safe, [Access] access  
Priority 3: [Zone] - [Survivors] people, [Safety]% safe, [Access] access

STEP 2️⃣ - RESOURCE ALLOCATION
Based on the priorities above, assign these teams:
- Fire_Alpha: Structural rescue specialists (8 members, heavy equipment)
- Medical_Beta: Emergency medical team (6 members, trauma expertise)
- K9_Gamma: Search and rescue (4 members, detection dogs)

Output format:
🔥 Fire_Alpha → Assigned to [Zone] - Task: [specific 10-word action]
⚕️ Medical_Beta → Assigned to [Zone] - Task: [specific 10-word action]
🐕 K9_Gamma → Assigned to [Zone] - Task: [specific 10-word action]

STEP 3️⃣ - 10-MINUTE COORDINATION TIMELINE
Create a minute-by-minute action plan:

Minutes 0-3: [Initial actions, team deployment]
Minutes 4-6: [Primary rescue operations]
Minutes 7-10: [Secondary operations, safety checks]

Include communication protocols and safety checkpoints specific to {scenario_type} scenarios.

Provide your complete response following this exact structure."""

        # Call Bedrock with inference profile
        bedrock_start = time.time()
        response = bedrock.invoke_model(
            modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2500,
                "messages": [{
                    "role": "user",
                    "content": prompt
                }],
                "temperature": 0.7
            })
        )
        bedrock_time = time.time() - bedrock_start
        
        # Parse response
        response_body = json.loads(response['body'].read())
        coordination_plan = response_body['content'][0]['text']
        
        # OPTION B: Calculate performance metrics
        total_execution_time = time.time() - start_time
        
        # Estimate tokens (rough approximation)
        estimated_input_tokens = len(prompt.split()) * 1.3  # Words to tokens rough estimate
        estimated_output_tokens = len(coordination_plan.split()) * 1.3
        total_tokens = estimated_input_tokens + estimated_output_tokens
        
        # Cost calculation (Claude 3.5 Sonnet pricing)
        # Input: $0.003 per 1K tokens, Output: $0.015 per 1K tokens
        estimated_cost = (estimated_input_tokens / 1000 * 0.003) + (estimated_output_tokens / 1000 * 0.015)
        
        # OPTION A: Log incident to memory
        incident_record = {
            'incident_id': f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'scenario_type': scenario_type,
            'scenario_hash': abs(hash(scenario[:50])) % 10000,
            'teams_deployed': ['Fire_Alpha', 'Medical_Beta', 'K9_Gamma'],
            'execution_time': round(total_execution_time, 2),
            'priority_zone_identified': True
        }
        INCIDENT_LOG.append(incident_record)
        
        print(f"✅ Coordination plan generated - Logged as {incident_record['incident_id']}")
        
        # Format final output with all enhancements
        final_output = f"""
╔═══════════════════════════════════════════════════════════════╗
║              RESCUESYNC AI DISASTER COORDINATOR              ║
║           Multi-Step Reasoning Architecture (v1.0)            ║
╚═══════════════════════════════════════════════════════════════╝

🎯 SCENARIO TYPE: {scenario_type.upper().replace('_', ' ')}
📋 INCIDENT ID: {incident_record['incident_id']}

{coordination_plan}

════════════════════════════════════════════════════════════════
📊 AGENT MEMORY & PERFORMANCE METRICS
════════════════════════════════════════════════════════════════

💾 PERSISTENT MEMORY (AgentCore Memory Simulation):
   • Total incidents coordinated this session: {len(INCIDENT_LOG)}
   • Current incident ID: {incident_record['incident_id']}
   • Session context maintained across {len(INCIDENT_LOG)} disaster responses
   • Previous incidents: {[log['incident_id'] for log in INCIDENT_LOG[:-1]] if len(INCIDENT_LOG) > 1 else 'None (first incident)'}

⚡ PERFORMANCE METRICS:
   • Total execution time: {round(total_execution_time, 2)} seconds
   • Bedrock inference time: {round(bedrock_time, 2)} seconds
   • Estimated tokens processed: ~{int(total_tokens)} tokens
   • Estimated cost: ${round(estimated_cost, 4)} USD
   • Tokens per second: {int(total_tokens / bedrock_time)}

🎯 OPTIMIZATION INSIGHTS:
   • Lambda cold start: {"Yes (first invocation)" if total_execution_time > 3 else "No (warm container)"}
   • Response latency: {"Excellent (<5s)" if total_execution_time < 5 else "Good (<15s)" if total_execution_time < 15 else "Acceptable"}
   • Cost efficiency: {"Optimal" if estimated_cost < 0.01 else "Standard"}

════════════════════════════════════════════════════════════════
🤖 System: RescueSync AI Agent
🧠 Model: Claude 3.5 Sonnet v2 (Inference Profile)
⚡ Platform: Amazon Bedrock + AWS Lambda
🎯 Architecture: Single-agent multi-step reasoning with persistent memory
🌐 Scenario Support: Building Collapse | Earthquake | Flood
════════════════════════════════════════════════════════════════
"""
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'coordination_plan': final_output,
                'agent': 'RescueSync v1.0 - Enhanced Multi-Step Reasoning',
                'model': 'claude-3.5-sonnet-v2',
                'inference_profile': 'us.anthropic.claude-3-5-sonnet-20241022-v2:0',
                'scenario_type': scenario_type,
                'architecture': 'Single-agent with structured reasoning + memory',
                'performance_metrics': {
                    'execution_time_seconds': round(total_execution_time, 2),
                    'bedrock_time_seconds': round(bedrock_time, 2),
                    'estimated_cost_usd': round(estimated_cost, 4),
                    'estimated_tokens': int(total_tokens),
                    'tokens_per_second': int(total_tokens / bedrock_time)
                },
                'memory_stats': {
                    'incident_id': incident_record['incident_id'],
                    'total_incidents_coordinated': len(INCIDENT_LOG),
                    'session_context_maintained': True
                }
            }, indent=2)
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Disaster coordination failed',
                'suggestion': 'Check CloudWatch logs for details'
            })
        }
