FROM public.ecr.aws/lambda/python:3.12

COPY core.py ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN cd ${LAMBDA_TASK_ROOT} && pip install -r requirements.txt

CMD ["main.handler"]