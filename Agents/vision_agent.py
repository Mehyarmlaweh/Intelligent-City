# pylint: disable=import-error
"business agent"
import os
import sys
from base_agent import BaseAgent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import Settings


class VisionAgent(BaseAgent):
    """InfrastructureAgent class for handling
    infrastructure planning and analysis"""

    def __init__(self, settings: Settings):
        """Initialize the InfrastructureAgent with configuration settings.

        Args:
            settings (Settings): Configuration settings instance
        """
        super().__init__(settings)

        self.collected_data = None
        self.environment = settings.ENVIRONMENT

    def collect_data(self, data: dict):
        """Collect data from the input dictionary.

        Args:
            data (dict): A dictionary containing
            infrastructure-related information.

        Raises:
            ValueError: If the input is not a dictionary.
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a dictionary")

        if data:
            self.collected_data = data

    def ask_llm(self):
        """Ask the LLM for generating.

        Args:
            None
        Returns:
            Img: An infrastructure image
        """
        # if not self.collected_data:
        #   return "Please provide infrastructure-related information."

        # Construct a prompt for the LLM
        prompts = self._construct_prompt()
        promptDallE1024Token = self.claude.invoke(prompts["prompt1"])
        image1Claude = self.claude.invoke(prompts["prompt2"])
        output = {}
        try:
            image2DallE = self.dallEclient.images.generate(
                model="dall-e-3",
                prompt=promptDallE1024Token.content,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            output["image1_DallE"] = image2DallE.data[0].url
            output["image2_Claude"] = image1Claude.content
            return output
        except Exception as e:
            if self.environment == "local":
                print(f"Error invoking Claude: {str(e)}")
            return "An error occurred while processing your request."

    def _construct_prompt(self) -> str:
        """Construct a prompt for generating natural-looking architectural site plans.

        Returns:
            str: The constructed prompt for SVG generation
        """
        prompts = {}
        prompts[
            "prompt1"
        ] = f"""
        As an expert architectural visualization system, generate a single detailed site plan image with a natural, hand-drawn quality. 

        Requirements from {self.collected_data}:
        1. Drawing Style:
        - Use organic, irregular paths for building footprints
        - Create natural curves for roads and paths
        - Add subtle shadows and depth
        - Include detailed landscape elements
        - Maintain architectural precision while avoiding rigid geometry

        2. Key Components:
        - Complex building shapes with angular geometries
        - Natural-looking tree placements along streets
        - Organic water features or green spaces
        - Detailed parking layouts
        - Pedestrian pathways
        - Site context and connections

        3. Technical Elements:
        - Scale: 1:1000
        - North arrow
        - Grid overlay (subtle, not dominant)
        - Clear legend
        - Building labels
        - Dimension lines where needed

        4. Color Palette:
        - Soft, architectural colors
        - Subtle shadows
        - Natural vegetation tones
        - Varied paving patterns
        - Water features in muted blues

    Create organic shapes using <path> elements with curved segments. Include shadow effects using subtle gradient fills. 

        Generate the image as a complete, professional architectural site plan that maintains the natural, 
        hand-drawn quality of traditional architectural drawings."""

        prompts[
            "prompt2"
        ] = f"""Generate a technical 2D architectural layout as an SVG image that can be saved and opened later 
    in browsers and vector editing software. Use the following structure and specifications:

                SVG TECHNICAL REQUIREMENTS:
                - Create SVG with xmlns="http://www.w3.org/2000/svg"
                - Set viewBox="0 0 1000 800" for standard dimensions
                - Use vector paths and basic shapes (rect, circle, path, line)
                - Implement proper grouping with <g> elements
                - Define reusable elements in <defs> section
                - Ensure all elements have proper stroke and fill attributes
                - Use standard RGB colors or named web colors
                - Include proper scaling for measurements

                COMPOSITION REQUIREMENTS:
                Layout Grid:
                - Implement grid using SVG <pattern> element
                - Each grid unit = one standard block
                - Include coordinate system with clear measurements
                - Add north arrow and scale bar as vector elements

                Required Elements (based on {self.collected_data}):
                1. Buildings and Facilities (use consistent styling):
                - Residential [R]: <rect> elements in rgb(173, 216, 230)
                - Commercial [C]: <rect> elements in rgb(255, 228, 181)
                - Mixed-use [M]: <rect> elements in rgb(147, 112, 219)
                - Schools [S]: <rect> with text element "S" in rgb(255, 255, 0)
                - Universities [U]: <rect> with text element "U" in rgb(255, 255, 0)
                - Hospitals [H]: <rect> with <path> cross in rgb(255, 0, 0)
                - Clinics [L]: <rect> with <path> cross in rgb(255, 182, 193)
                - Pharmacies [X]: <rect> with text element "Rx" in rgb(144, 238, 144)

                2. Public Spaces:
                - Parks [P]: <path> elements in rgb(144, 238, 144) with tree symbols
                - Squares [Q]: <path> elements in rgb(245, 245, 220)

                3. Transportation:
                - Bus Stops [B]: <circle> with text element "B"
                - Bike Lanes: <path stroke-dasharray="5,5">
                - EV Stations: Custom <path> lightning symbol
                - Streets: <path> elements in rgb(128, 128, 128)
                - Intersections: Composite shapes for traffic controls

                SVG ORGANIZATION:
                1. Define patterns and symbols in <defs>
                2. Create main layout groups:
                - Background grid
                - Infrastructure
                - Buildings
                - Transportation
                - Labels
                - Legend
                3. Use proper z-indexing for element layering

                LEGEND REQUIREMENTS:
                - Create as <g> element in top right
                - Use consistent styling with main elements
                - Include all symbols with labels
                - Add scale reference
                - List abbreviations

                TECHNICAL SPECIFICATIONS:
                - Use stroke-width consistently
                - Implement proper scaling
                - Create clear text elements
                - Mark entry/exit points
                - Show pedestrian paths

                SMART INFRASTRUCTURE:
                - Add infrastructure nodes as <circle> elements
                - Show sensor networks with small <circle> elements
                - Include utility connections as styled <path> elements
                - Mark emergency routes with distinct styling

                ENSURE SVG READABILITY:
                - Add proper class names to elements
                - Include descriptive IDs where needed
                - Organize related elements in groups
                - Use consistent naming conventions
                - Add minimal inline documentation

                Generate the layout as a complete, valid SVG
                that follows these specifications while
                incorporating all data from {self.collected_data}.
                The output should be directly saveable as a .svg 
                file and viewable in modern browsers and vector editors."""

        return prompts  
