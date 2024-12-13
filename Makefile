IMAGE_NAME := planning_poker
TEST_IMAGE_NAME := planning_poker_test
CONTAINER_NAME := planning_poker
TEST_CONTAINER_NAME := planning_poker_test
PORT := 8000

.PHONY: build start stop ensure-image-built ensure-not-running test-unit

build:
	docker build -t $(IMAGE_NAME):latest --target app .

ensure-image-built:
	@if [ -z "$$(docker images -q $(IMAGE_NAME):latest 2> /dev/null)" ]; then \
		echo "Image $(IMAGE_NAME):latest not found. Building..."; \
		make build; \
	fi

ensure-not-running:
	@if lsof -i :$(PORT) > /dev/null 2>&1; then \
		echo "Port $(PORT) is already in use. Attempting to stop existing container..."; \
		make stop; \
	fi

start: ensure-image-built ensure-not-running
	docker run -d --name=$(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME) -b 0.0.0.0:$(PORT) -w 1 "run:create_app()"

stop:
	@if docker ps -q -f name=$(CONTAINER_NAME); then \
		docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME); \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi


test-unit: ensure-image-built
	@echo "Building test image..."
	docker build -t $(TEST_IMAGE_NAME) --target test .
	@echo "Running tests..."
	docker run --rm --name=$(TEST_CONTAINER_NAME) -e PYTHONPATH="." $(TEST_IMAGE_NAME)
	@echo "Removing test image..."
	@if docker images -q $(TEST_IMAGE_NAME); then \
		docker image rm $(TEST_IMAGE_NAME); \
	else \
		echo "Test image $(TEST_IMAGE_NAME) not found."; \
	fi
