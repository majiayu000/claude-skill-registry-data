---
name: quarkus-native-test
description: Execute Quarkus native image tests using GraalVM/Mandrel builder. This skill should be used when users request to run native tests, validate native compilation, test GraalVM compatibility, or verify native image functionality for Quarkus applications.
---

# Quarkus Native Test Skill

## Purpose

This skill executes Quarkus native image tests using the GraalVM/Mandrel native-image compiler. Native testing validates that Quarkus applications compile correctly to native executables and function properly in GraalVM's substrate VM environment, which has different constraints than standard JVM execution.

## When to Use This Skill

Invoke this skill when users request:
- "Run native tests"
- "Test native compilation"
- "Validate GraalVM compatibility"
- "Execute native image tests"
- "Verify native functionality"
- "Check native build"
- "Test with Mandrel"
- Pre-deployment validation for native deployments
- Debugging native-specific issues (reflection, serialization, resource loading)

## What Native Testing Does

Native testing compiles the Quarkus application into a standalone native executable using GraalVM's ahead-of-time (AOT) compilation, then runs the test suite against this native binary. This process:

1. **Compiles to Native Code**: Uses GraalVM/Mandrel to compile Java bytecode directly to machine code
2. **Validates Reflection Configuration**: Ensures all reflection, resource access, and JNI calls are properly registered
3. **Tests Substrate VM Constraints**: Verifies the application works within GraalVM's closed-world assumptions
4. **Detects Native-Specific Issues**: Identifies problems that only occur in native mode (class initialization, static analysis limitations)
5. **Validates Performance**: Confirms fast startup times and low memory footprint characteristic of native images

## Native Test Command

Execute the following Maven command to run native tests:

```bash
./mvnw -V -B -am clean verify -Dnative -Dquarkus.native.builder-image=quay.io/quarkus/ubi9-quarkus-mandrel-builder-image:jdk-21
```

### Command Breakdown

- `./mvnw`: Uses Maven wrapper for consistent Maven version
- `-V`: Displays Maven version information
- `-B`: Batch mode (non-interactive, suitable for CI/CD)
- `-am`: Also make - builds dependent modules if in multi-module project
- `clean verify`: Clean previous builds and run all phases through integration testing
- `-Dnative`: Activates Quarkus native profile for native compilation
- `-Dquarkus.native.builder-image=quay.io/quarkus/ubi9-quarkus-mandrel-builder-image:jdk-21`: Specifies the container image for native compilation (Mandrel JDK 21 on UBI9)

## Execution Workflow

### Pre-Execution Validation

Before running native tests, verify:

1. **Docker/Podman Available**: Native builds require containerized builder
   ```bash
   docker --version || podman --version
   ```

2. **Sufficient Resources**: Native compilation is resource-intensive
   - Minimum: 4GB RAM, 2 CPU cores
   - Recommended: 8GB RAM, 4 CPU cores
   - Disk space: 2-5GB for build artifacts

3. **Clean State**: Ensure no stale build artifacts
   ```bash
   ./mvnw clean
   ```

### Expected Duration

Native tests take significantly longer than JVM tests:
- **Small Projects**: 2-5 minutes
- **Medium Projects**: 5-15 minutes
- **Large Projects**: 15-30+ minutes

Inform users of expected duration to set proper expectations.

### Execution Steps

1. **Display Execution Notice**
   ```
   Starting Quarkus native tests...
   This process compiles the application to native code and may take 5-15 minutes.
   Using Mandrel JDK 21 builder image for GraalVM compilation.
   ```

2. **Execute Command**
   ```bash
   ./mvnw -V -B -am clean verify -Dnative -Dquarkus.native.builder-image=quay.io/quarkus/ubi9-quarkus-mandrel-builder-image:jdk-21
   ```

3. **Monitor Progress**
   Watch for key compilation phases:
   - Dependency resolution
   - Java compilation
   - Native image build (longest phase)
   - Native test execution

4. **Validate Results**
   Check for:
   - `BUILD SUCCESS` message
   - All tests passing
   - Native executable created in `target/` directory

## Error Handling & Troubleshooting

### Common Issues and Resolutions

#### 1. Docker/Podman Not Available

**Symptom**: "Cannot run program 'docker'" or "No container runtime found"

**Resolution**:
- Install Docker Desktop or Podman
- Ensure Docker daemon is running
- Verify user has permissions to access Docker socket
- Alternative: Use local GraalVM installation with `-Dquarkus.native.container-build=false`

#### 2. Insufficient Memory

**Symptom**: "Error: Image build request failed" or Out of Memory errors during native-image compilation

**Resolution**:
- Increase Docker memory allocation (Docker Desktop settings)
- Add memory configuration: `-Dquarkus.native.native-image-xmx=4g`
- Close memory-intensive applications during build
- Consider using smaller builder image or reducing parallel builds

#### 3. Reflection Configuration Missing

**Symptom**: "ClassNotFoundException" or "NoSuchMethodException" in native tests that pass in JVM mode

**Resolution**:
- Check `src/main/resources/META-INF/native-image/reflect-config.json`
- Add missing reflection registrations
- Use Quarkus reflection annotations (@RegisterForReflection)
- Run with tracing agent to capture reflection usage: `-Dquarkus.native.enable-reports=true`

#### 4. Resource Loading Issues

**Symptom**: "Resource not found" errors in native mode

**Resolution**:
- Verify resources are in `src/main/resources/`
- Check `application.properties` for resource inclusion patterns
- Add resources to `quarkus.native.resources.includes` property
- Validate resource paths use forward slashes (not backslashes)

#### 5. Build Timeout

**Symptom**: Build hangs or times out during native-image phase

**Resolution**:
- Increase timeout: `-Dquarkus.native.build-timeout=PT30M` (30 minutes)
- Check Docker container has network access for dependency downloads
- Verify no antivirus software blocking container operations
- Review build logs for stuck dependency downloads

#### 6. Test Failures in Native Mode Only

**Symptom**: Tests pass in JVM mode but fail in native mode

**Resolution**:
- Check for dynamic class loading or reflection not registered
- Verify static initialization order (class initializers run at build time in native)
- Review test for JVM-specific assumptions (e.g., classpath scanning)
- Use `@DisabledInNativeImage` for tests incompatible with native mode
- Add native-specific test configuration in `application.properties` with `%native` profile

#### 7. Native Image Build Fails

**Symptom**: "Fatal error: Unsupported features" or analysis errors

**Resolution**:
- Review error messages for unsupported feature reports
- Check for libraries incompatible with GraalVM (e.g., JVMTI, JMX, dynamic proxies)
- Add substitutions for incompatible code
- Use `--initialize-at-run-time` for problematic classes
- Consult Quarkus extension compatibility matrix

## Success Validation

After native test execution completes successfully:

1. **Verify Build Success**
   - Check for `BUILD SUCCESS` in output
   - Confirm no test failures (0 failures, 0 errors, 0 skipped)

2. **Validate Native Executable**
   ```bash
   ls -lh target/*-runner
   ```
   - Native executable should exist
   - Size typically 50-150MB depending on dependencies

3. **Verify Test Coverage**
   - Ensure all critical paths tested in native mode
   - Check native test execution time (should be faster startup than JVM)

4. **Review Performance Metrics**
   - Startup time: < 100ms for small apps (vs seconds in JVM)
   - Memory usage: Lower RSS than JVM equivalent
   - Build time: Document for future reference

## Best Practices

### When to Run Native Tests

- **Pre-Commit**: For critical native-specific code changes
- **CI/CD Pipeline**: On pull requests and main branch commits
- **Pre-Release**: Always before production deployments
- **Regression Testing**: After dependency updates affecting native compilation
- **Investigation**: When debugging native-specific issues

### Optimization Tips

1. **Incremental Testing**: Run JVM tests first; only run native tests after JVM tests pass
2. **Parallel Builds**: Use `-Dquarkus.native.builder-image.pull=if-not-present` to cache builder image
3. **Resource Limits**: Configure appropriate memory limits for faster feedback
4. **Test Selection**: Use `-Dtest=SpecificTest` to run specific native tests during development
5. **Build Caching**: Leverage layer caching in CI/CD to reduce builder image pull time

### Native-Specific Testing Considerations

1. **Test Reflection**: Explicitly test all reflection-based functionality
2. **Resource Loading**: Verify all resource loading patterns work in native
3. **Serialization**: Test JSON/XML serialization with all DTOs
4. **Database Access**: Validate database drivers and connection pooling
5. **HTTP Clients**: Test REST clients and external service integration
6. **Message Brokers**: Verify MQTT/Kafka/RabbitMQ connectivity in native mode

## Project-Specific Context

This skill is configured for the **Quarkus HiveMQ Client** extension project:

- **Technology Stack**: Java, Quarkus, HiveMQ MQTT client, Maven
- **Native Requirements**: GraalVM/Mandrel JDK 21 compatibility
- **Critical Native Tests**: MQTT connection management, message publishing/subscribing, client lifecycle
- **Known Considerations**: HiveMQ client reflection configuration, netty native transport, SSL/TLS certificate loading

## Integration with Development Workflow

### Typical Usage Pattern

1. **Feature Development**: Develop feature with JVM testing
2. **Local Validation**: Run quick JVM tests (`./mvnw test`)
3. **Pre-Commit Check**: Run native tests before committing critical changes
4. **CI Validation**: Automated native testing in GitHub Actions/Jenkins
5. **Deployment Preparation**: Final native test run before release

### Skill Invocation Examples

User says: "Run native tests"
→ Execute native test command with progress monitoring

User says: "My native tests are failing but JVM tests pass"
→ Execute native tests with verbose logging, analyze differences, provide troubleshooting guidance

User says: "Validate the HiveMQ client works in native mode"
→ Execute native tests, verify MQTT-specific functionality, report native compatibility status

## Output Reporting

After execution, provide:

1. **Status Summary**: Success/failure with key metrics
2. **Execution Time**: Total duration and phase breakdown
3. **Test Results**: Tests run, passed, failed, skipped
4. **Build Artifacts**: Location and size of native executable
5. **Next Steps**: Recommendations based on results (e.g., investigate failures, commit changes, deploy)

## Additional Resources

- **Quarkus Native Guide**: https://quarkus.io/guides/building-native-image
- **GraalVM Native Image**: https://www.graalvm.org/latest/reference-manual/native-image/
- **Mandrel Project**: https://github.com/graalvm/mandrel
- **Quarkus Testing Guide**: https://quarkus.io/guides/getting-started-testing

---

**Maintained By**: Backend Engineer and Master Orchestrator
**Last Updated**: 2025-10-21
**Project Context**: Quarkus HiveMQ Client Extension - Native Image Validation