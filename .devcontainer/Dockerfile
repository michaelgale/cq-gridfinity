FROM condaforge/mambaforge:23.3.1-1

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install system dependencies
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git=1:2.* \
    libgl1-mesa-dev \
    xvfb \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Create conda environment and install packages
RUN mamba create -n cqdev python=3.12 -y \
    && mamba init bash \
    && mamba install -n cqdev -c conda-forge -y \
    cadquery=2.4 \
    pytest=8.* \
    black=24.* \
    flake8=7.* \
    isort=5.* \
    && mamba clean --all -f -y

# Install pip dependencies
SHELL ["/bin/bash", "-c"]
RUN source /opt/conda/etc/profile.d/conda.sh \
    && conda activate cqdev \
    && pip install --no-cache-dir \
    ezdxf \
    cqkit \
    importlib_metadata

# Install package in development mode
WORKDIR /workspaces/cq-gridfinity
RUN source /opt/conda/etc/profile.d/conda.sh \
    && conda activate cqdev \
    && pip install -e .

# Set up X11 and OpenGL
RUN mkdir -p /tmp/runtime-root \
    && chown ${USERNAME}:${USERNAME} /tmp/runtime-root
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV DISPLAY=:99
ENV LIBGL_ALWAYS_INDIRECT=1

# Configure conda environment
ENV PATH=/opt/conda/envs/cqdev/bin:$PATH
RUN echo "conda activate cqdev" >> /home/${USERNAME}/.bashrc

# Set up virtual framebuffer
COPY .devcontainer/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch to non-root user
USER ${USERNAME}

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["sleep", "infinity"] 