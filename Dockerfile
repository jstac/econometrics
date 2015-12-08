# Econometrics Book Docker Image
# User: jovyan
# This uses the Jupyter DataScience Docker Container with Python, R and Julia

FROM jupyter/datascience-notebook

MAINTAINER Matthew McKay <mamckay@gmail.com>

USER root

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