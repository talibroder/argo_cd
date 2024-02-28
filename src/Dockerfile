# Stage 1: Build stage

FROM python:3.9-slim as builder

WORKDIR /weather_deploy

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm -f requirements.txt

RUN pip install gunicorn



# Stage 2: Production stage

FROM builder 

WORKDIR /weather_deploy

# Copy the application source code from the previous stage
COPY --from=builder . .

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 weather_deploy:app 


