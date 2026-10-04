---
name: jade-recipe-8-11-corba-retrofit
description: >-
  Java 11 removed the java.corba module (JEP 320): org.omg.* classes no longer
  exist in the JDK. This recipe retrofits a standalone GlassFish CORBA
  implementation (omgapi + orb + transitive jars) into lib/corba/ and wires it
  into the Ant compile classpath so FIPA/* and jade.mtp.iiop/* compile and run
  on JDK 11. Idempotent. Removes JADE-FLAG:CORBA_REMOVAL markers.
  Invoked by jade-core-rule-dispatcher.
arguments: [--file, --line]
---
# jade-recipe-8-11-corba-retrofit

Ensures the CORBA retrofit is present and clears `JADE-FLAG:CORBA_REMOVAL`
markers. The jars are vendored under `lib/corba/` (resolved via Maven from
`org.glassfish.corba:glassfish-corba-orb:4.2.2`, which pulls the omgapi that
provides `org.omg.CORBA`). The recipe verifies the jar set, (re)applies the
`compile.classpath` path element in `build.xml` when missing, and removes the
next outstanding flag marker per invocation.