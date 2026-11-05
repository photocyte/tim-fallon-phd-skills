# LinkML modeling language

<!-- Modeled after Matt Pocock's https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling -->

Shared terminology for the LinkML setup and documentation skills. These definitions distinguish concepts that are easily conflated; they are not a replacement for the LinkML specification.

## Language

### Describing data

**Data model**:
A description of the entities, properties, relationships and meanings in a domain.
_Avoid_: Contract.

**Data specification**:
An explicit account of the data structure, meanings and validation rules expected for an exchange or use.
_Avoid_: Contract, when the intended meaning is data requirements.

**Schema**:
A machine-readable expression of a data model and its constraints in a schema language. LinkML documentation also uses “model” for a schema; use “schema” when the formal representation matters.

**Metamodel**:
The model defining the elements and rules of a modeling language. The LinkML metamodel describes LinkML schemas, rather than a particular application's records.
_Avoid_: Application schema, when referring to the language definition.

**Class**:
A schema definition describing a category of instances and their properties and constraints.

**Instance**:
A particular data object described by a class; a Person record is an instance, while Person is a class.
_Avoid_: Schema, when referring to a record.

**Slot**:
A property definition describing values or relationships associated with instances. A class-local attribute is a slot defined in that class's context.

**Type**:
A value domain for scalar values, such as strings or integers, potentially with additional constraints.
_Avoid_: Class, when referring to a scalar value domain.

**Enumeration**:
A definition of permitted values, either listed explicitly or specified through value-set rules.

**Range**:
The permitted category of a slot's values, expressed through a type, class or enumeration.

**Cardinality**:
The permitted number of values for a slot. It describes quantity, not whether related objects are embedded or referenced.

### Interpreting a schema

**Asserted schema**:
The definitions explicitly stated by the schema author.

**Derived schema**:
The effective definitions after applying the language's derivation rules, including inheritance and class-specific slot refinements.
_Avoid_: Generated JSON Schema, as a synonym; that is a different target representation.

**Identifier**:
A value denoting a particular instance, rather than its display label. Declared identity or uniqueness requirements are distinct from a validator's ability to enforce them.

**Instance reference**:
A value identifying another data object instead of embedding that object's contents.
_Avoid_: Schema reference or bibliographic reference, when the target is a data object.

**Inlined representation**:
A representation containing a related object's contents within the enclosing record, rather than only its identifier.

### Checking and changing data

**Schema validation**:
Checking whether a schema conforms to the language's metamodel and applicable rules.

**Instance validation**:
Checking data against a selected schema using a particular validation strategy. Passing establishes only the conditions that strategy actually checks, not factual correctness.
_Avoid_: Fully verified, for a structural validation result.

**Schema linting**:
Checking schema quality and conventions, such as naming consistency; a linting workflow may also include schema validation.

**Normalization**:
A transformation into a selected representation, potentially including type coercion or collection restructuring.
_Avoid_: Validation, when the operation changes the data being checked.

**Vocabulary mapping**:
A declared semantic relationship between concepts or schema elements, such as exact or close correspondence.
_Avoid_: Data transformation, when no executable conversion is specified.

**Data transformation**:
A conversion of instance data between structures, values or representations according to specified rules.

### Producing representations

**Schema generation**:
Deriving a target schema representation from a source schema. The target may express fewer constraints or annotations than the source.

**Schema documentation**:
A human-readable description of a schema's definitions and relationships.

**Instance rendering**:
A human-readable view of particular data records, such as a Markdown transcript.
_Avoid_: Schema documentation, when the output presents records rather than their definitions.
