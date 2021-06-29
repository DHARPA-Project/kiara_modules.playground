End-to-end network analysis pipeline, incl. data onboarding.

This pipeline reads network graph data from a csv file that contains edges data, as well as an optional csv file containing node attributes (and/or nodes that are not connected to other nodes.)

It then converts this data into a network graph structure, and extracts graph properties (like density, number of edges, number of nodes, ...) and graph component properties (largest component, number of components).

