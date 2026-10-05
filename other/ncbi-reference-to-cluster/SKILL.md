---
name: ncbi-reference-to-cluster
description: Select, document, download, and checksum-verify the most appropriate NCBI reference genome on an HPC cluster. Use whenever an analysis needs a reference genome, genome FASTA, genome annotation, assembly accession, or genome index and no exact approved assembly is already available; when a user asks to fetch a species genome from NCBI; or when a pipeline must resolve and cache a reproducible reference assembly on a remote cluster.
---

# NCBI Reference to Cluster

Resolve the exact assembly before analysis, download it directly on the cluster, and preserve enough provenance to reproduce the choice. Never interpret “best” as “largest N50” alone.

## Required inputs

Discover these from the request, repository, pipeline config, environment, or existing cluster files before asking:

- Organism: prefer NCBI Taxonomy ID or unambiguous scientific name.
- Compatibility constraints: required assembly accession/build, strain/isolate, haplotype, coordinate system, or annotation source.
- Cluster connection and destination root.
- Required files. Default to `genome,gff3,gtf,seq-report`; omit annotation formats the downstream tool does not use.

Ask only for missing information that cannot be safely inferred. Never invent a cluster host, account, filesystem path, strain, or assembly build. If the project or user pins an accession, treat it as authoritative and skip automatic ranking after confirming it is current.

## Workflow

1. Search local project and cluster caches for an existing exact accession plus provenance. Reuse it when checksums and required files are valid.
2. Confirm whether downstream compatibility requires a conventional build. For example, coordinate-based resources may require GRCh38 even if another human assembly is newer.
3. Check cluster policy and available commands without changing the system:
   - `datasets`, Python 3, SSH, scheduler conventions, destination permissions, quota, and free space.
   - Do not install software or write outside the approved destination without permission.
   - Run downloads in a scheduler job when cluster policy discourages work on login nodes.
4. Copy or stream `scripts/fetch_ncbi_reference.py` to the cluster. Run it first without `--yes` to produce a read-only candidate report and proposed destination.
5. Show the selected accession, the top alternatives, the reason for selection, included file types, and destination. Obtain confirmation before the first material download unless the user already explicitly approved this exact organism, destination, and selection policy.
6. Run the same command with `--yes` on the cluster.
7. Verify that the command reports `status: downloaded` or `status: already-present`, that NCBI MD5 checks pass, and that `provenance.json` exists.
8. Return the exact versioned accession and absolute cluster paths to FASTA, annotations, sequence report, and provenance. Update the pipeline config only when requested.

## Selection policy

Apply constraints before ranking:

1. Exact user/project accession or required build.
2. Exact species, strain/isolate, assembly source, and downstream coordinate compatibility.
3. Exclude suppressed, atypical, multi-isolate, and metagenome-assembled records by default.

Rank eligible cellular-organism assemblies lexicographically:

1. NCBI RefSeq category: `reference genome` > `representative genome` > unclassified.
2. Assembly level: complete genome > chromosome > scaffold > contig.
3. RefSeq (`GCF_`) > GenBank-only (`GCA_`).
4. Annotated > unannotated when annotation is needed.
5. Higher scaffold/contig N50, fewer contigs, and newer release date as tie-breakers.

Report the leading candidates rather than hiding the decision. Do not switch an established project to another accession merely because it scores higher.

For viruses, organelles, pangenomes, mixed taxa, hybrids, or strain-sensitive microbial work, do not apply the cellular assembly ranking blindly. Resolve the biological unit and downstream compatibility first; use the corresponding NCBI Datasets virus/organelle workflow or an explicit accession.

## Run the bundled script

Execute on the machine where the reference should reside:

```bash
python3 scripts/fetch_ncbi_reference.py \
  --taxon "Homo sapiens" \
  --dest-root /cluster/shared/references \
  --include genome,gff3,gtf,seq-report
```

The first run is a dry run. After reviewing its JSON report:

```bash
python3 scripts/fetch_ncbi_reference.py \
  --taxon "Homo sapiens" \
  --dest-root /cluster/shared/references \
  --include genome,gff3,gtf,seq-report \
  --yes
```

Use `--accession GCF_...` to honor a pinned assembly and repeat `--search VALUE` for a required strain, assembly name, or submitter. Read `python3 scripts/fetch_ncbi_reference.py --help` for all options.

## Safety and reproducibility

- Keep version suffixes such as `.40`; never reduce an accession to an unversioned alias.
- Do not overwrite an existing accession directory. A valid existing download is a no-op; an incomplete or conflicting directory is an error for manual review.
- Extract ZIP members safely, validate every entry in NCBI `md5sum.txt`, and publish the final directory atomically.
- Never expose an NCBI API key in commands or logs. Pass the name of an environment variable with `--api-key-env`.
- Preserve `provenance.json`, `candidate_report.json`, NCBI reports, and the original package ZIP unless storage policy requires removing the ZIP after verification.
- Build aligner indices only after the reference download is verified, and keep index provenance tied to the exact assembly accession and FASTA checksum.
