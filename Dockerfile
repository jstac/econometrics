# Econometrics Book Base Docker Image (for tmpnb orchestrate.py server)
# User: econ

FROM debian:jessie

MAINTAINER Matthew McKay <mamckay@gmail.com>

# Install all OS dependencies for fully functional notebook server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -yq --no-install-recommends \
    git \
    vim \
    wget \
    build-essential \
    python-dev \
    ca-certificates \
    bzip2 \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    supervisor \
    sudo \
    && apt-get clean

# Julia dependencies
RUN apt-get install -y julia libnettle4 && apt-get clean

# R dependencies that conda can't provide (X, fonts, compilers)
RUN apt-get install -y libzmq3-dev libcurl4-openssl-dev libxrender1 fonts-dejavu gfortran gcc && apt-get clean

ENV CONDA_DIR /opt/conda

# Install conda
RUN echo 'export PATH=$CONDA_DIR/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-3.9.1-Linux-x86_64.sh && \
    /bin/bash /Miniconda3-3.9.1-Linux-x86_64.sh -b -p $CONDA_DIR && \
    rm Miniconda3-3.9.1-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda install --yes conda==3.14.1

# We run our docker images with a non-root user as a security precaution.
# econ is our user
RUN useradd -m -s /bin/bash econ
RUN chown -R econ:econ $CONDA_DIR

EXPOSE 8888

USER econ
ENV HOME /home/econ
ENV SHELL /bin/bash
ENV USER econ
ENV PATH $CONDA_DIR/bin:$PATH
WORKDIR $HOME

RUN conda install --yes ipython-notebook terminado && conda clean -yt

RUN ipython profile create

# Workaround for issue with ADD permissions
USER root
ADD notebooks/ /home/econ/
RUN chown econ:econ /home/econ -R
USER econ

# Python packages
RUN conda install --yes pip numpy pandas scikit-learn scikit-image matplotlib scipy seaborn sympy cython patsy statsmodels cloudpickle dill numba bokeh && conda clean -yt

# Now for a python2 environment
#RUN conda create -p $CONDA_DIR/envs/python2 python=2.7 ipython numpy pandas scikit-learn scikit-image matplotlib scipy seaborn sympy cython patsy statsmodels cloudpickle dill numba bokeh && conda clean -yt
#RUN $CONDA_DIR/envs/python2/bin/python $CONDA_DIR/envs/python2/bin/ipython kernelspec install-self --user

#Install QuantEcon
RUN pip install quantecon
#RUN source activate python2 && pip install quantecon && source deactivate python2

# R packages
RUN conda config --add channels r
RUN conda install --yes r-irkernel r-plyr r-devtools r-rcurl r-dplyr r-ggplot2 r-caret rpy2 r-tidyr r-shiny r-rmarkdown r-forecast r-stringr r-rsqlite r-reshape2 r-nycflights13 r-randomforest && conda clean -yt

# IJulia and Julia packages
RUN julia -e 'Pkg.add("IJulia")'
RUN julia -e 'Pkg.add("Gadfly")' && julia -e 'Pkg.add("RDatasets")' && julia -e 'Pkg.add("PyPlot")' && julia -e 'Pkg.add("Distributions")' && julia -e 'Pkg.add("KernelEstimator")' 

# Convert notebooks to the current format
RUN find /home/. -name '*.ipynb' -exec ipython nbconvert --to notebook {} --output {} \;
RUN find /home/. -name '*.ipynb' -exec ipython trust {} \;

CMD ipython notebook
