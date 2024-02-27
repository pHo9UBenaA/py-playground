# py-playground

This repository serves as a playground for learning and experimenting with Python. Follow the steps below to set up the environment and run sample scripts.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/pHo9UBenaA/py-playground.git
cd py-playground
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running Sample Scripts

The `scripts` directory contains sample Python scripts. You can run them using:

```bash
python scripts/your_script.py
```

## Using Docker for Environment Setup

Alternatively, you can use Docker to set up the environment. Follow these steps:

### 1. Build the Docker Image

```bash
docker-compose build
```

### 2. Start the Container

```bash
docker-compose up -d
```

### 3. Access the Container

To execute scripts inside the container, enter the following command:

```bash
docker-compose exec python bash
```

Once inside the container, you can run Python scripts as usual.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details. 
