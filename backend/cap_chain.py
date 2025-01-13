# # cap_chain.py
# from typing import List, Dict
# import google.generativeai as genai

# class CaptioningChain:
#     """Enhanced chain for image captioning using dual Gemini models"""
    
#     def __init__(self, model1, model2):
#         self.primary_model = model1
#         self.secondary_model = model2
#         self._init_prompts()

#     def _init_prompts(self):
#         """Initialize detailed prompts for each component"""
#         self.prompts = {
#             "base_description": """
#             Generate detailed, descriptive captions for the provided image using the following structured format. Each caption should be thorough, objective, and follow these specific guidelines:
#             """,
#             "Required Sections": """
#             1. Summary (15-25 words)
#                 - Briefly identify the primary subject(s), location, and main action
#                 - Focus on the most immediately noticeable elements
#                 - Use present tense and active voice
#             2. Subject: People, Objects, and Actions (100-200 words)
#                 - Describe all visible people with:
#                     - Physical appearance (skin tone, hair style/color, visible features)
#                     - Clothing details (style, color, fit)
#                     - Body language and expressions
#                     - Actions and positioning
#                     - Interactions with others or objects
#                 - For objects:
#                     - Specific names and descriptions
#                     - Colors, materials, and conditions
#                     - Placement and arrangement
#                     - Quantity when relevant
#                 - Maintain neutral, objective language
#                 - Avoid assumptions about characteristics not visibly apparent
#             3. Environment and Background (70-200 words)
#             - Describe the setting in detail:
#                 - Indoor/outdoor location specifics
#                 - Lighting conditions and sources
#                 - Time of day/weather if apparent
#                 - Architectural or natural elements
#                 - Spatial relationships between elements
#                 - Background and foreground details
#                 - Overall atmosphere and mood created by the environment
#             4. Photo Attributes (50-70 words)
#                 - Technical aspects:
#                     - Camera angle (low, eye-level, high, etc.)
#                     - Shot type (close-up, medium, wide)
#                     - Depth of field
#                     - Lighting quality and direction
#                 - Creative elements:
#                     - Composition details
#                     - Color palette and temperature
#                     - Overall mood and emotional impact
#                 - Visual effects or post-processing if apparent
#             """,
#             "Important Guidelines": """
#                 - Use present tense throughout
#                 - Maintain objective, neutral tone
#                 - Focus only on visibly apparent details
#                 - Use specific, descriptive language
#                 - Avoid subjective interpretations or assumptions
#                 - Include relevant technical photography terms
#                 - Describe spatial relationships clearly
#                 - Note any significant patterns or repetitions
#                 - Maintain professional, respectful language
#                 - Avoid brand names unless essential to description
#                 - Use inclusive and neutral terminology for describing people
#                 - Note significant lighting effects and their impact on the scene
#             """,
#             "Formatting Requirements": """
#                 - Present sections in the specified order
#                 - Label each section clearly
#                 - Use complete sentences
#                 - Maintain consistent voice throughout
#                 - Avoid repetitive phrase structures
#                 - Include appropriate transitions between elements
#                 - Use proper grammar and punctuation
#                 - Avoid abbreviations
#             """,
#             "Restrictions": """
#                 - No mature, abusive, or illegal content
#                 - No assumptions about non-visible characteristics
#                 - No subjective quality judgments
#                 - No brand names or commercial references
#                 - No technical specifications unless visible
#                 - No personal interpretations of subjects' thoughts or feelings
#                 - No references to other images or comparisons
#             """,
#         }

#     def _generate_with_context(self, image, prompt: str, 
#                              context: Dict[str, str] = None) -> str:
#         """Generate content with context awareness"""
#         if context:
#             enhanced_prompt = f"""
#             Previous Analysis Context:
#             {str(context)}
            
#             New Analysis Task:
#             {prompt}
#             """
#         else:
#             enhanced_prompt = prompt
            
#         # Alternate between models for load balancing
#         model = self.primary_model if len(context or {}) % 2 == 0 else self.secondary_model
#         response = model.generate_content([enhanced_prompt, image])
#         return response.text

#     def __call__(self, inputs: Dict) -> Dict[str, str]:
#         """Execute the chain with enhanced context handling"""
#         image = inputs["image"]
#         results = {}
#         context = {}
        
#         # Generate components sequentially with context
#         for key, prompt in self.prompts.items():
#             results[key] = self._generate_with_context(image, prompt, context)
#             context[key] = results[key]
        
#         return results

####################################################################################################
####################################################################################################
# # cap_chain.py
# from typing import Dict
# # import google.generativeai as genai
# from PIL import Image

# class CaptioningChain:
#     """Enhanced chain for image captioning using dual Gemini Vision models"""
    
#     def __init__(self, model1, model2):
#         self.primary_model = model1
#         self.secondary_model = model2
#         self._init_prompts()

#     def _init_prompts(self):
#         """Initialize detailed prompts for each component"""
#         self.prompts = {
#             "base_description": """
#             Provide a clear, factual description of the key elements visible in this image.
#             Focus on the main subjects, actions, and setting in 2-3 sentences.
#             """,
#             "detailed_analysis": """
#             Please provide a detailed analysis of this image with the following sections:

#             1. Subject Analysis (People, Objects, Actions):
#             - Describe all visible people, their appearance, clothing, and actions
#             - Detail important objects, their characteristics and placement
#             - Note any significant interactions or movements

#             2. Environment and Setting:
#             - Describe the location and surroundings
#             - Note lighting conditions and atmosphere
#             - Identify any notable background elements

#             3. Technical Aspects:
#             - Camera angle and shot type
#             - Lighting quality and direction
#             - Composition and framing
#             - Any notable photographic techniques used

#             Be objective and focus only on visible elements.
#             """,
#             "final_summary": """
#             Create a comprehensive yet concise summary (2-3 sentences) that captures:
#             - The key visual elements and their relationships
#             - The overall mood and impact of the image
#             - Any notable or unique aspects
#             """
#         }

#     def _generate_with_context(self, image: Image.Image, prompt: str, 
#                              context: Dict[str, str] = None) -> str:
#         """Generate content with context awareness"""
#         # Construct the complete prompt
#         if context:
#             enhanced_prompt = f"""
#             Previous Analysis Context:
#             {str(context)}
            
#             New Analysis Task:
#             {prompt}
#             """
#         else:
#             enhanced_prompt = prompt
            
#         # Alternate between models for load balancing
#         model = self.primary_model if len(context or {}) % 2 == 0 else self.secondary_model
        
#         try:
#             response = model.generate_content([enhanced_prompt, image])
#             return response.text
#         except Exception as e:
#             raise Exception(f"Image analysis failed: {str(e)}")

#     def __call__(self, inputs: Dict) -> Dict[str, str]:
#         """Execute the chain with enhanced context handling"""
#         image = inputs["image"]
#         results = {}
#         context = {}
        
#         # Generate components sequentially with context
#         for key, prompt in self.prompts.items():
#             results[key] = self._generate_with_context(image, prompt, context)
#             context[key] = results[key]
        
#         return results

########################################################################
# cap_chain.py
from typing import Dict, Tuple
from PIL import Image

class CaptioningChain:
    """Enhanced chain for image captioning using dual Gemini Vision models with token tracking"""
    
    def __init__(self, model1, model2):
        self.primary_model = model1
        self.secondary_model = model2
        self._init_prompts()

    def _init_prompts(self):
        """Initialize detailed prompts for each component"""
        self.prompts = {
            "base_description": """
            Provide a clear, factual description of the key elements visible in this image.
            Focus on the main subjects, actions, and setting in 2-3 sentences.
            """,
            "detailed_analysis": """
            Please provide a detailed analysis of this image with the following sections:

            1. Subject Analysis (People, Objects, Actions):
            - Describe all visible people, their appearance, clothing, color of their skin and actions
            - Detail important objects, their characteristics and placement
            - Note any significant interactions or movements

            2. Environment and Setting:
            - Describe the location and surroundings
            - Note lighting conditions and atmosphere
            - Identify any notable background elements

            3. Technical Aspects:
            - Camera angle and shot type
            - Lighting quality and direction
            - Composition and framing
            - Any notable photographic techniques used

            Be objective and focus only on visible elements.
            """,
            "final_summary": """
            Create a comprehensive yet concise summary (2-3 sentences) that captures:
            - The key visual elements and their relationships
            - The overall mood and impact of the image
            - Any notable or unique aspects
            """
        }

    def _generate_with_context(self, image: Image.Image, prompt: str, 
                             context: Dict[str, str] = None) -> Tuple[str, Dict[str, int]]:
        """Generate content with context awareness and return token usage"""
        # Construct the complete prompt
        if context:
            enhanced_prompt = f"""
            Previous Analysis Context:
            {str(context)}
            
            New Analysis Task:
            {prompt}
            """
        else:
            enhanced_prompt = prompt
            
        # Alternate between models for load balancing
        model = self.primary_model if len(context or {}) % 2 == 0 else self.secondary_model
        
        try:
            response = model.generate_content([enhanced_prompt, image])
            
            # Get token usage from response
            token_usage = {
                'prompt_tokens': response.prompt_tokens if hasattr(response, 'prompt_tokens') else 0,
                'completion_tokens': response.completion_tokens if hasattr(response, 'completion_tokens') else 0,
                'total_tokens': response.total_tokens if hasattr(response, 'total_tokens') else 0
            }
            
            return response.text, token_usage
        except Exception as e:
            raise Exception(f"Image analysis failed: {str(e)}")

    def __call__(self, inputs: Dict) -> Tuple[Dict[str, str], Dict[str, int]]:
        """Execute the chain with enhanced context handling and token tracking"""
        image = inputs["image"]
        results = {}
        context = {}
        token_usage = {'key1': 0, 'key2': 0}  # Track tokens for each key
        
        # Generate components sequentially with context
        for i, (key, prompt) in enumerate(self.prompts.items()):
            result, usage = self._generate_with_context(image, prompt, context)
            results[key] = result
            context[key] = result
            
            # Accumulate token usage for appropriate key
            key_num = 'key1' if i % 2 == 0 else 'key2'
            token_usage[key_num] += usage['total_tokens']
        
        return results, token_usage