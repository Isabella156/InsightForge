## InsightForge

InsightForge is a command-line interface (CLI) program designed to assist developers in generating Solidity code that is amenable for Mythril verification, leveraging the capabilities of ChatGPT.

### Features

- **Code Generation**: Automatically generates Solidity code using ChatGPT based on user inputs.
- **Instrument Code**: Integrate with Scribble to automatically instrument code.
- **Verification**: Integrates with Mythril to verify the correctness and security of the generated Solidity code.

### Prerequisites

- Docker installed on your machine (See [Docker Installation Guide](https://docs.docker.com/get-docker/))
- An OpenAI API key for using ChatGPT services

### Installation

1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone git@github.com:Isabella156/InsightForge.git
   cd InsightForge
   ```

2. **Build the Docker Image**

   Build the Docker image using the provided Dockerfile:

   ```bash
   docker build -t insightforge .
   ```

### Usage

To run the main InsightForge application:

```bash
docker run -it -e OPENAI_API_KEY='your-openai-api-key' insightforge
```

This command starts the InsightForge application in an interactive Docker container, enabling you to interact with ChatGPT for Solidity code generation. `demo/demo.md` provide example commands to run the application.

### Pipeline Demonstration

For users interested in viewing the entire process from code generation to verification, an alternate Docker image can be built that targets the pipeline demonstration:

1. **Modify the Dockerfile**

   Change the command in the Dockerfile to use the pipeline script:

   ```Dockerfile
   CMD ["python", "./src/pipeline.py"]
   ```

2. **Build the Pipeline Docker Image**

   ```bash
   docker build -t insightforge-pipeline .
   ```

3. **Run the Pipeline Image**

   ```bash
   docker run -it -e OPENAI_API_KEY='your-openai-api-key' insightforge-pipeline
   ```

This setup executes the complete pipeline, demonstrating how InsightForge generates Solidity code and then verifies it using Mythril within the Docker environment.

### Configurations

- **API Key**: Ensure you replace `'your-openai-api-key'` with your actual OpenAI API key in the Docker run command.