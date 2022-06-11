FROM public.ecr.aws/lambda/python:3.8
COPY . ./
RUN yum install -y gcc python27 python27-devel postgresql-devel
RUN python -m pip install -r requirements.txt
RUN [ "python", "-c", "import nltk; nltk.download('vader_lexicon')" ]
RUN cp -r /root/nltk_data /usr/local/share/nltk_data 
CMD [ "app.handler"]