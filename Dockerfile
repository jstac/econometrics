# Econometrics Book Docker Image
# User: jovyan
# This uses the Jupyter DataScience Docker Container with Python, R and Julia

FROM jupyter/datascience-notebook

MAINTAINER Matthew McKay <mamckay@gmail.com>

USER root

#-Additional Python Packages-#
RUN pip install quantecon
RUN $CONDA_DIR/envs/python2/bin/pip install quantecon

#-Additional Julia Packages-#
RUN julia -e 'Pkg.update()' && julia -e 'Pkg.build("IJulia")'
RUN julia -e 'Pkg.add("PyPlot")' && julia -e 'Pkg.add("Distributions")' && julia -e 'Pkg.add("KernelEstimator")'

#-Add Notebooks-#
ADD notebooks/ /home/jovyan/work/

#-Add Templates-#
ADD jupyter_notebook_config.py /home/jovyan/.jupyter/
ADD templates/ /srv/templates/
RUN chmod a+rX /srv/templates

#-Convert notebooks to the current format-#
RUN find /home/. -name '*.ipynb' -exec jupyter nbconvert --to notebook {} --output {} \;
RUN find /home/. -name '*.ipynb' -exec jupyter trust {} \;

USER jovyan