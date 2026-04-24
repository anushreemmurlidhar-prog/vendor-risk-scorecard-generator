FROM maven:3.9.5-eclipse-temurin-17 AS build
WORKDIR /workspace
COPY pom.xml ./
COPY src ./src
RUN mvn -B package -DskipTests

FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /workspace/target/tool93-0.0.1-SNAPSHOT.jar ./tool93.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "tool93.jar"]
