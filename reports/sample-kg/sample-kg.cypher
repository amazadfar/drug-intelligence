// Uniqueness constraints
CREATE CONSTRAINT drug_id_unique IF NOT EXISTS FOR (n:Drug) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT drugtype_id_unique IF NOT EXISTS FOR (n:DrugType) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT interaction_id_unique IF NOT EXISTS FOR (n:Interaction) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT mechanism_id_unique IF NOT EXISTS FOR (n:Mechanism) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT severity_id_unique IF NOT EXISTS FOR (n:Severity) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT reference_id_unique IF NOT EXISTS FOR (n:Reference) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT moleculefeature_id_unique IF NOT EXISTS FOR (n:MoleculeFeature) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT source_id_unique IF NOT EXISTS FOR (n:Source) REQUIRE n.id IS UNIQUE;

// Nodes
MERGE (n:Drug {id: "drug:synthetic-acetic-acid"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-acetic-acid", id: "drug:synthetic-acetic-acid", name: "Synthetic Acetic Acid Fixture", normalized_name: "synthetic_acetic_acid", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-acetone"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-acetone", id: "drug:synthetic-acetone", name: "Synthetic Acetone Fixture", normalized_name: "synthetic_acetone", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-aspirin-like"})
SET n += {description: "Hand-authored fixture resembling a small molecule record. Not copied from a restricted database.", drug_id: "synthetic-aspirin-like", id: "drug:synthetic-aspirin-like", name: "Synthetic Aspirin-Like Molecule", normalized_name: "synthetic_aspirin_like", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-benzene"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-benzene", id: "drug:synthetic-benzene", name: "Synthetic Benzene Fixture", normalized_name: "synthetic_benzene", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-caffeine-like"})
SET n += {description: "Hand-authored fixture for public schema and chemistry tests. Not copied from a restricted database.", drug_id: "synthetic-caffeine-like", id: "drug:synthetic-caffeine-like", name: "Synthetic Caffeine-Like Molecule", normalized_name: "synthetic_caffeine_like", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-cyclohexane"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-cyclohexane", id: "drug:synthetic-cyclohexane", name: "Synthetic Cyclohexane Fixture", normalized_name: "synthetic_cyclohexane", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-ethanol"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-ethanol", id: "drug:synthetic-ethanol", name: "Synthetic Ethanol Fixture", normalized_name: "synthetic_ethanol", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-ethylamine"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-ethylamine", id: "drug:synthetic-ethylamine", name: "Synthetic Ethylamine Fixture", normalized_name: "synthetic_ethylamine", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-phenol"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-phenol", id: "drug:synthetic-phenol", name: "Synthetic Phenol Fixture", normalized_name: "synthetic_phenol", source: "synthetic"};
MERGE (n:Drug {id: "drug:synthetic-pyridine"})
SET n += {description: "Hand-authored chemistry fixture with no interaction claim.", drug_id: "synthetic-pyridine", id: "drug:synthetic-pyridine", name: "Synthetic Pyridine Fixture", normalized_name: "synthetic_pyridine", source: "synthetic"};
MERGE (n:DrugType {id: "drug_type:small_molecule"})
SET n += {id: "drug_type:small_molecule", name: "small_molecule", source: "synthetic"};
MERGE (n:Interaction {id: "interaction:synthetic-int-001"})
SET n += {evidence: "Synthetic fixture only. No clinical claim is implied.", id: "interaction:synthetic-int-001", interaction_id: "synthetic-int-001", source: "synthetic"};
MERGE (n:Mechanism {id: "mechanism:metabolism"})
SET n += {id: "mechanism:metabolism", name: "metabolism", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-acetic-acid"})
SET n += {id: "molecule_feature:synthetic-acetic-acid", representation: "CC(=O)O", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-acetone"})
SET n += {id: "molecule_feature:synthetic-acetone", representation: "CC(=O)C", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-aspirin-like"})
SET n += {id: "molecule_feature:synthetic-aspirin-like", representation: "CC(=O)OC1=CC=CC=C1C(=O)O", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-benzene"})
SET n += {id: "molecule_feature:synthetic-benzene", representation: "c1ccccc1", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-caffeine-like"})
SET n += {id: "molecule_feature:synthetic-caffeine-like", representation: "Cn1cnc2n(C)c(=O)n(C)c(=O)c12", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-cyclohexane"})
SET n += {id: "molecule_feature:synthetic-cyclohexane", representation: "C1CCCCC1", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-ethanol"})
SET n += {id: "molecule_feature:synthetic-ethanol", representation: "CCO", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-ethylamine"})
SET n += {id: "molecule_feature:synthetic-ethylamine", representation: "CCN", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-phenol"})
SET n += {id: "molecule_feature:synthetic-phenol", representation: "Oc1ccccc1", representation_type: "smiles", source: "synthetic"};
MERGE (n:MoleculeFeature {id: "molecule_feature:synthetic-pyridine"})
SET n += {id: "molecule_feature:synthetic-pyridine", representation: "n1ccccc1", representation_type: "smiles", source: "synthetic"};
MERGE (n:Reference {id: "reference:synthetic-ref-001"})
SET n += {abstract: "This hand-authored fixture exists only to exercise evidence schemas.", id: "reference:synthetic-ref-001", reference_id: "synthetic-ref-001", source: "synthetic", title: "Synthetic fixture reference for drug intelligence examples"};
MERGE (n:Severity {id: "severity:1"})
SET n += {id: "severity:1", level: 1, name: "minor", source: "synthetic"};
MERGE (n:Source {id: "source:synthetic"})
SET n += {id: "source:synthetic", name: "synthetic"};

// Relationships
MATCH (source {id: "drug:synthetic-acetic-acid"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-acetic-acid:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-acetic-acid:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-acetic-acid"})
MATCH (target {id: "molecule_feature:synthetic-acetic-acid"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-acetic-acid:has_molecular_feature:molecule_feature:synthetic-acetic-acid"}]->(target)
SET r += {id: "drug:synthetic-acetic-acid:has_molecular_feature:molecule_feature:synthetic-acetic-acid", source: "synthetic"};
MATCH (source {id: "drug:synthetic-acetic-acid"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-acetic-acid:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-acetic-acid:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-acetone"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-acetone:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-acetone:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-acetone"})
MATCH (target {id: "molecule_feature:synthetic-acetone"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-acetone:has_molecular_feature:molecule_feature:synthetic-acetone"}]->(target)
SET r += {id: "drug:synthetic-acetone:has_molecular_feature:molecule_feature:synthetic-acetone", source: "synthetic"};
MATCH (source {id: "drug:synthetic-acetone"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-acetone:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-acetone:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-aspirin-like"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-aspirin-like:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-aspirin-like:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-aspirin-like"})
MATCH (target {id: "molecule_feature:synthetic-aspirin-like"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-aspirin-like:has_molecular_feature:molecule_feature:synthetic-aspirin-like"}]->(target)
SET r += {id: "drug:synthetic-aspirin-like:has_molecular_feature:molecule_feature:synthetic-aspirin-like", source: "synthetic"};
MATCH (source {id: "drug:synthetic-aspirin-like"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-aspirin-like:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-aspirin-like:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-benzene"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-benzene:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-benzene:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-benzene"})
MATCH (target {id: "molecule_feature:synthetic-benzene"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-benzene:has_molecular_feature:molecule_feature:synthetic-benzene"}]->(target)
SET r += {id: "drug:synthetic-benzene:has_molecular_feature:molecule_feature:synthetic-benzene", source: "synthetic"};
MATCH (source {id: "drug:synthetic-benzene"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-benzene:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-benzene:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-caffeine-like"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-caffeine-like:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-caffeine-like:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-caffeine-like"})
MATCH (target {id: "molecule_feature:synthetic-caffeine-like"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-caffeine-like:has_molecular_feature:molecule_feature:synthetic-caffeine-like"}]->(target)
SET r += {id: "drug:synthetic-caffeine-like:has_molecular_feature:molecule_feature:synthetic-caffeine-like", source: "synthetic"};
MATCH (source {id: "drug:synthetic-caffeine-like"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-caffeine-like:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-caffeine-like:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-cyclohexane"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-cyclohexane:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-cyclohexane:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-cyclohexane"})
MATCH (target {id: "molecule_feature:synthetic-cyclohexane"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-cyclohexane:has_molecular_feature:molecule_feature:synthetic-cyclohexane"}]->(target)
SET r += {id: "drug:synthetic-cyclohexane:has_molecular_feature:molecule_feature:synthetic-cyclohexane", source: "synthetic"};
MATCH (source {id: "drug:synthetic-cyclohexane"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-cyclohexane:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-cyclohexane:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-ethanol"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-ethanol:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-ethanol:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-ethanol"})
MATCH (target {id: "molecule_feature:synthetic-ethanol"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-ethanol:has_molecular_feature:molecule_feature:synthetic-ethanol"}]->(target)
SET r += {id: "drug:synthetic-ethanol:has_molecular_feature:molecule_feature:synthetic-ethanol", source: "synthetic"};
MATCH (source {id: "drug:synthetic-ethanol"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-ethanol:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-ethanol:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-ethylamine"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-ethylamine:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-ethylamine:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-ethylamine"})
MATCH (target {id: "molecule_feature:synthetic-ethylamine"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-ethylamine:has_molecular_feature:molecule_feature:synthetic-ethylamine"}]->(target)
SET r += {id: "drug:synthetic-ethylamine:has_molecular_feature:molecule_feature:synthetic-ethylamine", source: "synthetic"};
MATCH (source {id: "drug:synthetic-ethylamine"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-ethylamine:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-ethylamine:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-phenol"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-phenol:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-phenol:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-phenol"})
MATCH (target {id: "molecule_feature:synthetic-phenol"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-phenol:has_molecular_feature:molecule_feature:synthetic-phenol"}]->(target)
SET r += {id: "drug:synthetic-phenol:has_molecular_feature:molecule_feature:synthetic-phenol", source: "synthetic"};
MATCH (source {id: "drug:synthetic-phenol"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-phenol:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-phenol:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "drug:synthetic-pyridine"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "drug:synthetic-pyridine:derived_from:synthetic"}]->(target)
SET r += {id: "drug:synthetic-pyridine:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "drug:synthetic-pyridine"})
MATCH (target {id: "molecule_feature:synthetic-pyridine"})
MERGE (source)-[r:HAS_MOLECULAR_FEATURE {id: "drug:synthetic-pyridine:has_molecular_feature:molecule_feature:synthetic-pyridine"}]->(target)
SET r += {id: "drug:synthetic-pyridine:has_molecular_feature:molecule_feature:synthetic-pyridine", source: "synthetic"};
MATCH (source {id: "drug:synthetic-pyridine"})
MATCH (target {id: "drug_type:small_molecule"})
MERGE (source)-[r:HAS_TYPE {id: "drug:synthetic-pyridine:has_type:drug_type:small_molecule"}]->(target)
SET r += {id: "drug:synthetic-pyridine:has_type:drug_type:small_molecule", source: "synthetic"};
MATCH (source {id: "interaction:synthetic-int-001"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "interaction:synthetic-int-001:derived_from:synthetic"}]->(target)
SET r += {id: "interaction:synthetic-int-001:derived_from:synthetic", source: "synthetic"};
MATCH (source {id: "interaction:synthetic-int-001"})
MATCH (target {id: "mechanism:metabolism"})
MERGE (source)-[r:HAS_MECHANISM {id: "interaction:synthetic-int-001:has_mechanism:metabolism"}]->(target)
SET r += {id: "interaction:synthetic-int-001:has_mechanism:metabolism", source: "synthetic"};
MATCH (source {id: "interaction:synthetic-int-001"})
MATCH (target {id: "severity:1"})
MERGE (source)-[r:HAS_SEVERITY {id: "interaction:synthetic-int-001:has_severity:metabolism:1"}]->(target)
SET r += {id: "interaction:synthetic-int-001:has_severity:metabolism:1", mechanism: "metabolism", source: "synthetic"};
MATCH (source {id: "interaction:synthetic-int-001"})
MATCH (target {id: "drug:synthetic-aspirin-like"})
MERGE (source)-[r:INVOLVES {id: "interaction:synthetic-int-001:involves:a:synthetic-aspirin-like"}]->(target)
SET r += {id: "interaction:synthetic-int-001:involves:a:synthetic-aspirin-like", role: "a", source: "synthetic"};
MATCH (source {id: "interaction:synthetic-int-001"})
MATCH (target {id: "drug:synthetic-caffeine-like"})
MERGE (source)-[r:INVOLVES {id: "interaction:synthetic-int-001:involves:b:synthetic-caffeine-like"}]->(target)
SET r += {id: "interaction:synthetic-int-001:involves:b:synthetic-caffeine-like", role: "b", source: "synthetic"};
MATCH (source {id: "interaction:synthetic-int-001"})
MATCH (target {id: "reference:synthetic-ref-001"})
MERGE (source)-[r:SUPPORTED_BY {id: "interaction:synthetic-int-001:supported_by:synthetic-ref-001"}]->(target)
SET r += {id: "interaction:synthetic-int-001:supported_by:synthetic-ref-001", source: "synthetic"};
MATCH (source {id: "reference:synthetic-ref-001"})
MATCH (target {id: "source:synthetic"})
MERGE (source)-[r:DERIVED_FROM {id: "reference:synthetic-ref-001:derived_from:synthetic"}]->(target)
SET r += {id: "reference:synthetic-ref-001:derived_from:synthetic", source: "synthetic"};

// Sample queries
// List synthetic drug interactions with mechanisms and severities.
MATCH (interaction:Interaction)-[:INVOLVES]->(drug:Drug)
OPTIONAL MATCH (interaction)-[:HAS_MECHANISM]->(mechanism:Mechanism)
OPTIONAL MATCH (interaction)-[severityRel:HAS_SEVERITY]->(severity:Severity)
RETURN interaction.id AS interaction_id,
       collect(DISTINCT drug.name) AS drugs,
       collect(DISTINCT mechanism.name) AS mechanisms,
       collect(DISTINCT {mechanism: severityRel.mechanism, severity: severity.name}) AS severities;

// Trace provenance for interaction facts.
MATCH (interaction:Interaction)-[:DERIVED_FROM]->(source:Source)
RETURN interaction.id AS interaction_id, source.name AS source;
