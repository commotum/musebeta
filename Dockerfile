FROM tensorflow/tensorflow:1.15.5-gpu-py3

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NVIDIA_REQUIRE_CUDA="cuda>=8.0" \
    LANG=C.UTF-8

WORKDIR /usr/src/app
COPY . .


RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - && apt-get install -y nodejs && npm run install && npm run build && rm -rf frontend


EXPOSE 8000

ENTRYPOINT npm run start