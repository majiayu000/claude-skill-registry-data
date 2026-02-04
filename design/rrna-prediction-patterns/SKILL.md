---
name: rrna-prediction-patterns
description: Guidelines for rRNA detection and prediction including prokaryotic (16S, 23S, 5S) and eukaryotic (18S, 28S, 5.8S, 5S) ribosomal RNA. Covers sequence patterns, secondary structure, HMM models, blast-based detection, length validation, and quality scoring for rRNA identification.
---

# rRNA Prediction Patterns

## Purpose

Provide comprehensive guidance for implementing rRNA (ribosomal RNA) detection and prediction in both prokaryotic and eukaryotic organisms. This skill helps ensure accurate identification, proper validation, and robust handling of rRNA sequences.

## When to Use

This skill activates when:
- Working with rRNA detection or prediction code
- Implementing sequence analysis for 16S, 18S, 23S, 28S, 5S, or 5.8S rRNA
- Building or using HMM models for ribosomal RNA
- Processing genomic sequences for rRNA identification
- Writing code in `backend/rrna/` or related directories
- Handling BLAST searches for rRNA sequences
- Validating rRNA sequence quality or completeness

## rRNA Types Overview

### Prokaryotic rRNA
- **16S rRNA**: ~1,500 bp, small subunit (SSU), most commonly used for phylogenetics
- **23S rRNA**: ~2,900 bp, large subunit (LSU)
- **5S rRNA**: ~120 bp, small ribosomal component

### Eukaryotic rRNA
- **18S rRNA**: ~1,800 bp, small subunit (SSU), equivalent to prokaryotic 16S
- **28S rRNA**: ~3,300-5,000 bp, large subunit (LSU)
- **5.8S rRNA**: ~160 bp, unique to eukaryotes
- **5S rRNA**: ~120 bp, similar to prokaryotic version

## Core Detection Methods

### 1. Hidden Markov Models (HMM)

**Best Practice**: Use established HMM profiles from databases like Rfam or create custom profiles.

```python
from hmmer import HMMer

def detect_rrna_with_hmm(sequence: str, rrna_type: str) -> dict:
    """
    Detect rRNA using HMM profiles.

    Args:
        sequence: DNA/RNA sequence
        rrna_type: One of ['16S', '18S', '23S', '28S', '5S', '5.8S']

    Returns:
        Detection results with score, e-value, and coordinates
    """
    hmm_profile = load_hmm_profile(rrna_type)

    results = HMMer.search(
        profile=hmm_profile,
        sequence=sequence,
        e_value_threshold=1e-5
    )

    return {
        'detected': results.has_hits(),
        'score': results.best_score,
        'e_value': results.best_e_value,
        'start': results.best_hit.start if results.has_hits() else None,
        'end': results.best_hit.end if results.has_hits() else None,
        'confidence': calculate_confidence(results.best_score)
    }
```

**Key Considerations**:
- Use appropriate e-value thresholds (typically 1e-5 to 1e-10)
- Validate sequence length against expected ranges
- Check for partial vs. complete genes
- Consider domain-specific models (bacteria, archaea, eukarya)

### 2. BLAST-Based Detection

**Best Practice**: Use specialized rRNA databases like SILVA or RDP.

```python
from Bio.Blast import NCBIWWW, NCBIXML

def blast_search_rrna(sequence: str, db: str = "silva") -> list:
    """
    Search for rRNA using BLAST against specialized databases.

    Args:
        sequence: Query sequence
        db: Database name (silva, rdp, greengenes)

    Returns:
        List of matches with identity, coverage, and annotation
    """
    result_handle = NCBIWWW.qblast(
        program="blastn",
        database=db,
        sequence=sequence,
        hitlist_size=10,
        expect=1e-5
    )

    matches = []
    for record in NCBIXML.parse(result_handle):
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                if hsp.identities / hsp.align_length > 0.85:  # 85% identity
                    matches.append({
                        'hit_def': alignment.hit_def,
                        'identity': hsp.identities / hsp.align_length,
                        'coverage': hsp.align_length / record.query_length,
                        'e_value': hsp.expect,
                        'rrna_type': extract_rrna_type(alignment.hit_def)
                    })

    return matches
```

**Key Considerations**:
- Minimum 85% identity for reliable rRNA identification
- Coverage should be >70% for full-length predictions
- Parse hit definitions carefully to extract rRNA type
- Handle ambiguous matches (multiple possible types)

### 3. Pattern-Based Detection

**Best Practice**: Use conserved sequence motifs and secondary structure patterns.

```python
import re
from typing import List, Tuple

# Conserved regions in 16S rRNA
CONSERVED_16S_PATTERNS = {
    'v1_region': r'GACGA[ACT]G[AG][ACT]TGCGA',
    'v3_region': r'GTGGAGGATGAAGG[CT]TTA',
    'v4_region': r'TAGC[CT]GGCGGAC',
    'shine_dalgarno_region': r'[AG]GGAGG',
}

def detect_conserved_regions(sequence: str, rrna_type: str) -> dict:
    """
    Detect conserved sequence patterns specific to rRNA types.

    Args:
        sequence: DNA sequence
        rrna_type: Type of rRNA to search for

    Returns:
        Dictionary of detected regions with positions
    """
    patterns = get_patterns_for_type(rrna_type)
    detected_regions = {}

    for region_name, pattern in patterns.items():
        matches = list(re.finditer(pattern, sequence, re.IGNORECASE))
        if matches:
            detected_regions[region_name] = [
                {'start': m.start(), 'end': m.end(), 'sequence': m.group()}
                for m in matches
            ]

    return detected_regions
```

**Conserved Regions to Check**:
- **16S**: V1-V9 variable regions flanked by conserved regions
- **18S**: V2, V4, V7, V9 regions
- **23S/28S**: Peptidyl transferase center, GTPase-associated center
- **5S**: Highly conserved sequence throughout

### 4. Length Validation

**Critical**: Always validate sequence length against expected ranges.

```python
LENGTH_RANGES = {
    '16S': {'min': 1200, 'max': 1800, 'typical': 1500},
    '18S': {'min': 1600, 'max': 2000, 'typical': 1800},
    '23S': {'min': 2500, 'max': 3200, 'typical': 2900},
    '28S': {'min': 3000, 'max': 5500, 'typical': 4000},
    '5S': {'min': 100, 'max': 140, 'typical': 120},
    '5.8S': {'min': 140, 'max': 180, 'typical': 160},
}

def validate_rrna_length(sequence: str, predicted_type: str) -> dict:
    """
    Validate if sequence length matches expected rRNA type.

    Returns:
        Validation result with completeness assessment
    """
    length = len(sequence)
    ranges = LENGTH_RANGES.get(predicted_type)

    if not ranges:
        return {'valid': False, 'reason': 'Unknown rRNA type'}

    completeness = length / ranges['typical']

    return {
        'valid': ranges['min'] <= length <= ranges['max'],
        'length': length,
        'expected_range': (ranges['min'], ranges['max']),
        'completeness': min(completeness, 1.0),
        'status': get_completeness_status(completeness)
    }

def get_completeness_status(completeness: float) -> str:
    """Classify sequence completeness."""
    if completeness >= 0.95:
        return 'complete'
    elif completeness >= 0.70:
        return 'nearly_complete'
    elif completeness >= 0.40:
        return 'partial'
    else:
        return 'fragment'
```

## Quality Scoring

**Best Practice**: Implement multi-factor quality scoring for predictions.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class RRNAQuality:
    """Quality metrics for rRNA prediction."""
    hmm_score: float
    blast_identity: Optional[float]
    length_validity: bool
    completeness: float
    conserved_regions_found: int
    total_conserved_regions: int

    def overall_quality(self) -> str:
        """Calculate overall quality classification."""
        score = 0

        # HMM score contribution (0-40 points)
        if self.hmm_score > 100:
            score += 40
        elif self.hmm_score > 50:
            score += 30
        elif self.hmm_score > 20:
            score += 20

        # BLAST identity contribution (0-30 points)
        if self.blast_identity:
            if self.blast_identity > 0.95:
                score += 30
            elif self.blast_identity > 0.85:
                score += 20
            elif self.blast_identity > 0.75:
                score += 10

        # Length validity (0-10 points)
        if self.length_validity:
            score += 10

        # Completeness (0-10 points)
        score += self.completeness * 10

        # Conserved regions (0-10 points)
        if self.total_conserved_regions > 0:
            ratio = self.conserved_regions_found / self.total_conserved_regions
            score += ratio * 10

        # Classify based on score
        if score >= 80:
            return 'high'
        elif score >= 60:
            return 'medium'
        elif score >= 40:
            return 'low'
        else:
            return 'very_low'

def score_rrna_prediction(
    sequence: str,
    hmm_results: dict,
    blast_results: list,
    predicted_type: str
) -> RRNAQuality:
    """
    Comprehensive quality scoring for rRNA prediction.

    Args:
        sequence: The predicted rRNA sequence
        hmm_results: Results from HMM search
        blast_results: Results from BLAST search
        predicted_type: Predicted rRNA type

    Returns:
        RRNAQuality object with detailed metrics
    """
    length_validation = validate_rrna_length(sequence, predicted_type)
    conserved = detect_conserved_regions(sequence, predicted_type)

    best_blast_identity = None
    if blast_results:
        best_blast_identity = max(r['identity'] for r in blast_results)

    return RRNAQuality(
        hmm_score=hmm_results.get('score', 0),
        blast_identity=best_blast_identity,
        length_validity=length_validation['valid'],
        completeness=length_validation['completeness'],
        conserved_regions_found=len(conserved),
        total_conserved_regions=get_expected_conserved_count(predicted_type),
    )
```

## Secondary Structure Considerations

**Important**: rRNA has complex secondary structures that aid in identification.

```python
def predict_secondary_structure(sequence: str) -> dict:
    """
    Predict secondary structure features of rRNA.

    Uses RNA folding algorithms to identify stems, loops, and hairpins
    characteristic of rRNA.
    """
    # Use ViennaRNA or similar
    from RNA import fold

    structure, mfe = fold(sequence)

    features = {
        'structure': structure,
        'mfe': mfe,  # Minimum free energy
        'stem_loops': count_stem_loops(structure),
        'hairpins': count_hairpins(structure),
        'internal_loops': count_internal_loops(structure),
    }

    # Validate against expected secondary structure
    return validate_secondary_structure(features, expected_for_rrna_type)
```

**Key Secondary Structure Features**:
- **16S/18S**: Highly conserved stems (helices 1-50 for 16S)
- **23S/28S**: Peptidyl transferase center with specific folding
- **5S**: Alpha-helix, loop, beta-helix pattern
- **5.8S**: Specific interaction sites with 28S

## Error Handling

**Critical**: Handle ambiguous and failed predictions gracefully.

```python
class RRNADetectionError(Exception):
    """Base exception for rRNA detection errors."""
    pass

class AmbiguousRRNATypeError(RRNADetectionError):
    """Raised when multiple rRNA types match equally well."""
    def __init__(self, candidates: List[str]):
        self.candidates = candidates
        super().__init__(f"Ambiguous rRNA type: {', '.join(candidates)}")

class NoRRNADetectedError(RRNADetectionError):
    """Raised when no rRNA is detected in sequence."""
    pass

def detect_rrna_with_error_handling(sequence: str) -> dict:
    """
    Detect rRNA with comprehensive error handling.

    Returns:
        Detection results or error information
    """
    try:
        # Try multiple methods
        hmm_results = {}
        blast_results = []

        for rrna_type in ['16S', '18S', '23S', '28S', '5S', '5.8S']:
            try:
                hmm_results[rrna_type] = detect_rrna_with_hmm(sequence, rrna_type)
            except Exception as e:
                # Log but continue
                log_detection_error(rrna_type, 'hmm', str(e))

        # Determine best match
        best_matches = [
            (rtype, results['score'])
            for rtype, results in hmm_results.items()
            if results['detected']
        ]

        if not best_matches:
            raise NoRRNADetectedError("No rRNA detected by any method")

        # Sort by score
        best_matches.sort(key=lambda x: x[1], reverse=True)

        # Check for ambiguity
        if len(best_matches) > 1:
            if best_matches[0][1] - best_matches[1][1] < 10:  # Similar scores
                raise AmbiguousRRNATypeError([m[0] for m in best_matches[:2]])

        predicted_type = best_matches[0][0]

        # Additional validation
        blast_results = blast_search_rrna(sequence)
        quality = score_rrna_prediction(
            sequence,
            hmm_results[predicted_type],
            blast_results,
            predicted_type
        )

        return {
            'success': True,
            'predicted_type': predicted_type,
            'quality': quality.overall_quality(),
            'details': {
                'hmm': hmm_results[predicted_type],
                'blast': blast_results,
                'quality_metrics': quality,
            }
        }

    except AmbiguousRRNATypeError as e:
        return {
            'success': False,
            'error_type': 'ambiguous',
            'candidates': e.candidates,
            'message': str(e),
            'suggestion': 'Try additional validation methods or manual inspection'
        }

    except NoRRNADetectedError as e:
        return {
            'success': False,
            'error_type': 'not_detected',
            'message': str(e),
            'suggestion': 'Sequence may not contain rRNA or quality may be too low'
        }

    except Exception as e:
        return {
            'success': False,
            'error_type': 'unknown',
            'message': str(e),
            'suggestion': 'Check sequence format and input parameters'
        }
```

## Best Practices Summary

### ✅ DO
- Use multiple detection methods (HMM + BLAST + patterns)
- Validate sequence length against expected ranges
- Calculate comprehensive quality scores
- Handle ambiguous predictions gracefully
- Check for conserved sequence regions
- Consider secondary structure when uncertain
- Use domain-specific databases (SILVA, RDP, Rfam)
- Log all detection attempts for debugging
- Provide confidence scores with predictions
- Test against known rRNA sequences

### ❌ DON'T
- Rely on a single detection method
- Ignore length validation
- Accept predictions without quality assessment
- Assume all detections are accurate
- Skip error handling for edge cases
- Use generic BLAST databases for rRNA
- Forget to handle partial sequences
- Mix up prokaryotic and eukaryotic types
- Ignore ambiguous matches
- Skip validation of conserved regions

## Common Pitfalls

1. **Pseudogenes**: Some genomic regions resemble rRNA but are non-functional
   - Solution: Check for stop codons, frameshifts in surrounding ORFs

2. **Contamination**: Sample may contain rRNA from multiple organisms
   - Solution: Cluster sequences by similarity before classification

3. **Chimeras**: PCR artifacts can create hybrid rRNA sequences
   - Solution: Use chimera detection tools (UCHIME, ChimeraSlayer)

4. **Partial Sequences**: Fragmented assemblies may contain incomplete rRNA
   - Solution: Report completeness percentage, handle fragments explicitly

## Testing Strategy

```python
# Example test cases
def test_rrna_detection():
    """Test suite for rRNA detection."""

    # Test case 1: Known 16S sequence
    ecoli_16s = load_sequence("test_data/ecoli_16s.fasta")
    result = detect_rrna_with_error_handling(ecoli_16s)
    assert result['success']
    assert result['predicted_type'] == '16S'
    assert result['quality'] in ['high', 'medium']

    # Test case 2: Known 18S sequence
    human_18s = load_sequence("test_data/human_18s.fasta")
    result = detect_rrna_with_error_handling(human_18s)
    assert result['predicted_type'] == '18S'

    # Test case 3: Non-rRNA sequence
    random_seq = generate_random_dna(1000)
    result = detect_rrna_with_error_handling(random_seq)
    assert not result['success']
    assert result['error_type'] == 'not_detected'

    # Test case 4: Partial rRNA
    partial_16s = ecoli_16s[:800]  # First 800bp only
    result = detect_rrna_with_error_handling(partial_16s)
    if result['success']:
        assert result['details']['quality_metrics'].status == 'partial'
```

---

**Related Skills**: [phylogenetic-methods](../phylogenetic-methods/SKILL.md)

**External Resources**:
- Rfam database: https://rfam.org/
- SILVA rRNA database: https://www.arb-silva.de/
- Ribosomal Database Project: https://rdp.cme.msu.edu/

**Line Count**: < 500 lines ✅
