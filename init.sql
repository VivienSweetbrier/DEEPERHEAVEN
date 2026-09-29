-- Project Deeper Heaven - init.sql
-- High-concurrency schema for PostgreSQL with PostGIS

-- Ensure PostGIS extension is enabled for GEOMETRY types
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create the 'units' table
-- Using UUIDs for primary keys to mitigate sequence-contention bottlenecks 
-- when 1,000+ async workers are writing simultaneously.
CREATE TABLE IF NOT EXISTS units (
    unit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    spinal_catastrophism_level INTEGER NOT NULL DEFAULT 0,
    tactical_grid_location GEOMETRY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraint to ensure trauma levels remain valid
    CONSTRAINT chk_spinal_catastrophism_level CHECK (spinal_catastrophism_level >= 0)
);

-- Spatial index (GiST) for the tactical grid GEOMETRY column
CREATE INDEX IF NOT EXISTS idx_units_tactical_grid_location 
    ON units USING GIST (tactical_grid_location);

-- Create the 'demons' (Naphtodemons) table
CREATE TABLE IF NOT EXISTS demons (
    demon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    oil_saturation_index NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    host_unit_id UUID REFERENCES units(unit_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index the foreign key to avoid lock contention and full table scans 
-- on 'demons' when 'units' records are modified or deleted.
CREATE INDEX IF NOT EXISTS idx_demons_host_unit_id 
    ON demons(host_unit_id);
