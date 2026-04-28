
ARG NODE_VERSION=22.16.0

################################################################################
# Use node image for base image for all stages.
FROM node:${NODE_VERSION}-alpine

# Set working directory for all build stages.
WORKDIR /client

COPY package*.json ./

RUN npm install 


# Copy the rest of the source files into the image.
COPY . .


# Expose the port that the application listens on.
EXPOSE 5173

# Run the application.
CMD ["npm", "run", "dev" , "--", "--host"]
