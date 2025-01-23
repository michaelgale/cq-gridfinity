FROM condaforge/mambaforge:latest

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git \
    libgl1-mesa-dev \
    xvfb \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Create conda environment
RUN mamba create -n cqdev python=3.12 -y \
    && mamba init bash

# Install CadQuery and dependencies via mamba
RUN mamba install -n cqdev -c conda-forge -y \
    cadquery=2.4 \
    pytest \
    black \
    flake8 \
    isort

# Install cqkit via pip
RUN source /opt/conda/etc/profile.d/conda.sh \
    && conda activate cqdev \
    && pip install cqkit

# Create XDG runtime directory
RUN mkdir -p /tmp/runtime-root
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV DISPLAY=:99
ENV LIBGL_ALWAYS_INDIRECT=1

# Activate conda environment by default
ENV PATH=/opt/conda/envs/cqdev/bin:$PATH
SHELL ["/bin/bash", "-c"]
RUN echo "conda activate cqdev" >> ~/.bashrc

# Set up virtual framebuffer
RUN printf '#!/bin/bash\nsource /opt/conda/etc/profile.d/conda.sh\nconda activate cqdev\nXvfb :99 -screen 0 1024x768x16 &\nsleep 1\nexec "$@"' > /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"] 