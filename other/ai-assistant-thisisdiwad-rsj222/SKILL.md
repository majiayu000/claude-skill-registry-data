---
name: ai-assistant
description: "Build AI assistant application with NLU, dialog management, and integrations"
---
apiVersion: v1
kind: Service
metadata:
  name: ai-assistant-service
spec:
  selector:
    app: ai-assistant
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ai-assistant-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ai-assistant
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
''',
            'caching_strategy': self._design_caching_strategy(),
            'load_balancing': self._design_load_balancing()
        }

    def _design_caching_strategy(self):
        """Design caching for performance"""
        return '''
class AssistantCache:
    def __init__(self):
        self.response_cache = ResponseCache()
        self.model_cache = ModelCache()
        self.context_cache = ContextCache()

    async def get_cached_response(self,
                                 message: str,
                                 context_hash: str) -> Optional[str]:
        """Get cached response if available"""
        cache_key = self.generate_cache_key(message, context_hash)

        # Check response cache
        cached = await self.response_cache.get(cache_key)
        if cached and not self.is_expired(cached):
            return cached['response']

        return None

    def cache_response(self,
                      message: str,
                      context_hash: str,
                      response: str,
                      ttl: int = 3600):
        """Cache response with TTL"""
        cache_key = self.generate_cache_key(message, context_hash)

        self.response_cache.set(
            cache_key,
            {
                'response': response,
                'timestamp': datetime.now(),
                'ttl': ttl
            }
        )

    def preload_model_cache(self):
        """Preload frequently used models"""
        models_to_cache = [
            'intent_classifier',
            'entity_extractor',
            'response_generator'
        ]

        for model_name in models_to_cache:
            model = load_model(model_name)
            self.model_cache.store(model_name, model)
'''
```

### 9. Monitoring and Analytics

Monitor assistant performance:

**Assistant Analytics System**

```python
class AssistantAnalytics:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.analytics_engine = AnalyticsEngine()

    def create_monitoring_dashboard(self):
        """Create monitoring dashboard configuration"""
        return {
            'real_time_metrics': {
                'active_sessions': 'gauge',
                'messages_per_second': 'counter',
                'response_time_p95': 'histogram',
                'intent_accuracy': 'gauge',
                'fallback_rate': 'gauge'
            },
            'conversation_metrics': {
                'avg_conversation_length': 'gauge',
                'completion_rate': 'gauge',
                'user_satisfaction': 'gauge',
                'escalation_rate': 'gauge'
            },
            'system_metrics': {
                'model_inference_time': 'histogram',
                'cache_hit_rate': 'gauge',
                'error_rate': 'counter',
                'resource_utilization': 'gauge'
            },
            'alerts': [
                {
                    'name': 'high_fallback_rate',
                    'condition': 'fallback_rate > 0.2',
                    'severity': 'warning'
                },
                {
                    'name': 'slow_response_time',
                    'condition': 'response_time_p95 > 2000',
                    'severity': 'critical'
                }
            ]
        }

    def analyze_conversation_quality(self):
        """Analyze conversation quality metrics"""
        return '''
class ConversationQualityAnalyzer:
    def analyze_conversations(self, time_range: str):
        """Analyze conversation quality"""
        conversations = self.fetch_conversations(time_range)

        metrics = {
            'intent_recognition': self.analyze_intent_accuracy(conversations),
            'response_relevance': self.analyze_response_relevance(conversations),
            'conversation_flow': self.analyze_conversation_flow(conversations),
            'user_satisfaction': self.analyze_satisfaction(conversations),
            'error_patterns': self.identify_error_patterns(conversations)
        }

        return self.generate_quality_report(metrics)

    def identify_improvement_areas(self, analysis):
        """Identify areas for improvement"""
        improvements = []

        # Low intent accuracy
        if analysis['intent_recognition']['accuracy'] < 0.85:
            improvements.append({
                'area': 'Intent Recognition',
                'issue': 'Low accuracy in intent detection',
                'recommendation': 'Retrain intent classifier with more examples',
                'priority': 'high'
            })

        # High fallback rate
        if analysis['conversation_flow']['fallback_rate'] > 0.15:
            improvements.append({
                'area': 'Coverage',
                'issue': 'High fallback rate',
                'recommendation': 'Expand training data for uncovered intents',
                'priority': 'medium'
            })

        return improvements
'''
```

### 10. Continuous Improvement

Implement continuous improvement cycle:

**Improvement Pipeline**

```python
class ContinuousImprovement:
    def create_improvement_pipeline(self):
        """Create continuous improvement pipeline"""
        return {
            'data_collection': '''
class ConversationDataCollector:
    async def collect_feedback(self, session_id: str):
        """Collect user feedback"""
        feedback_prompt = {
            'satisfaction': 'How satisfied were you with this conversation? (1-5)',
            'resolved': 'Was your issue resolved?',
            'improvements': 'How could we improve?'
        }

        feedback = await self.prompt_user_feedback(
            session_id,
            feedback_prompt
        )

        # Store feedback
        await self.store_feedback({
            'session_id': session_id,
            'timestamp': datetime.now(),
            'feedback': feedback,
            'conversation_metadata': self.get_session_metadata(session_id)
        })

        return feedback

    def identify_training_opportunities(self):
        """Identify conversations for training"""
        # Find low-confidence interactions
        low_confidence = self.find_low_confidence_interactions()

        # Find failed conversations
        failed = self.find_failed_conversations()

        # Find highly-rated conversations
        exemplary = self.find_exemplary_conversations()

        return {
            'needs_improvement': low_confidence + failed,
            'good_examples': exemplary
        }
''',
            'model_retraining': '''
class ModelRetrainer:
    async def retrain_models(self, new_data):
        """Retrain models with new data"""
        # Prepare training data
        training_data = self.prepare_training_data(new_data)

        # Validate data quality
        validation_result = self.validate_training_data(training_data)
        if not validation_result['passed']:
            return {'error': 'Data quality check failed', 'issues': validation_result['issues']}

        # Retrain models
        models_to_retrain = ['intent_classifier', 'entity_extractor']

        for model_name in models_to_retrain:
            # Load current model
            current_model = self.load_model(model_name)

            # Create new version
            new_model = await self.train_model(
                model_name,
                training_data,
                base_model=current_model
            )

            # Evaluate new model
            evaluation = await self.evaluate_model(
                new_model,
                self.get_test_set()
            )

            # Deploy if improved
            if evaluation['performance'] > current_model.performance:
                await self.deploy_model(new_model, model_name)

        return {'status': 'completed', 'models_updated': models_to_retrain}
''',
            'a_b_testing': '''
class ABTestingFramework:
    def create_ab_test(self,
                      test_name: str,
                      variants: List[Dict[str, Any]],
                      metrics: List[str]):
        """Create A/B test for assistant improvements"""
        test = {
            'id': generate_test_id(),
            'name': test_name,
            'variants': variants,
            'metrics': metrics,
            'allocation': self.calculate_traffic_allocation(variants),
            'duration': self.estimate_test_duration(metrics)
        }

        # Deploy test
        self.deploy_test(test)

        return test

    async def analyze_test_results(self, test_id: str):
        """Analyze A/B test results"""
        data = await self.collect_test_data(test_id)

        results = {}
        for metric in data['metrics']:
            # Statistical analysis
            analysis = self.statistical_analysis(
                data['control'][metric],
                data['variant'][metric]
            )

            results[metric] = {
                'control_mean': analysis['control_mean'],
                'variant_mean': analysis['variant_mean'],
                'lift': analysis['lift'],
                'p_value': analysis['p_value'],
                'significant': analysis['p_value'] < 0.05
            }

        return results
'''
        }
```

## Output Format

1. **Architecture Design**: Complete AI assistant architecture with components
2. **NLP Implementation**: Natural language processing pipeline and models
3. **Conversation Flows**: Dialog management and flow design
4. **Response Generation**: Intelligent response creation with LLM integration
5. **Context Management**: Sophisticated context and state management
6. **Testing Framework**: Comprehensive testing for conversational AI
7. **Deployment Guide**: Scalable deployment architecture
8. **Monitoring Setup**: Analytics and performance monitoring
9. **Improvement Pipeline**: Continuous improvement processes

Focus on creating production-ready AI assistants that provide real value through natural conversations, intelligent responses, and continuous learning from user interactions.

## Output Format

```xml
<result>
  <analysis>Brief analysis</analysis>
  <solution>Implementation</solution>
  <considerations>Trade-offs and notes</considerations>
</result>
```
