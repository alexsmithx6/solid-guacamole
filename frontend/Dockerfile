# Use the official Node.js image as a base image
FROM node:22-alpine

# Set the working directory in the container
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React application
RUN npm run build

# Start the React application
CMD ["npm", "start"]
