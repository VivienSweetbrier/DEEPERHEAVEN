# 🧦⚙️🧦 DEEPER HEAVEN: INFRASTRUCTURE VERIFICATION 

## Hostile QA Report
The initial subagent drafts were subjected to the Universal Verification Engine. They failed.
1. **DevOps Failure**: The subagent failed to mount the `init.sql` into the Postgres entrypoint. The database would have booted completely empty.
2. **Database Architect Failure**: The subagent failed to establish a `UNIQUE` constraint on the `units` table, meaning the requested `ON CONFLICT` concurrency lock would fail to trigger, resulting in duplicate inserts under heavy load.

*I have corrected the architecture below. The iron is now secure.*

## 1. Container Orchestration (`docker-compose.yml`)
```yaml
version: '3.8'

services:
  postgres:
    image: postgis/postgis:15-3.4
    environment:
      POSTGRES_USER: deeper_heaven
      POSTGRES_PASSWORD: deeper_password
      POSTGRES_DB: deeper_heaven_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      # FIX: Mounting the init.sql to ensure the database schema compiles on boot
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  python-worker:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgres://deeper_heaven:deeper_password@postgres:5432/deeper_heaven_db
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

volumes:
  postgres_data:
  redis_data:
```

## 2. The Theological Schema (`init.sql`)
```sql
-- Project Deeper Heaven
-- High-concurrency schema for PostgreSQL with PostGIS

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- THE UNITS TABLE (The Host Bodies)
CREATE TABLE IF NOT EXISTS units (
    unit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    callsign VARCHAR(255) NOT NULL UNIQUE, -- FIX: Unique constraint for ON CONFLICT DO UPDATE
    spinal_catastrophism_level INTEGER NOT NULL DEFAULT 0,
    tactical_grid_location GEOMETRY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_spinal_catastrophism_level CHECK (spinal_catastrophism_level >= 0)
);

-- Spatial index for nearest-neighbor Eldila targeting
CREATE INDEX IF NOT EXISTS idx_units_tactical_grid_location 
    ON units USING GIST (tactical_grid_location);

-- THE DEMONS TABLE (The Cyclonopedia Naphtodemons)
CREATE TABLE IF NOT EXISTS demons (
    demon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    oil_saturation_index NUMERIC(10, 4) NOT NULL DEFAULT 0.0,
    host_unit_id UUID REFERENCES units(unit_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_demons_host_unit_id ON demons(host_unit_id);

-- CONCURRENCY IMMUNITY PROOF (The Upsert Protocol)
-- When 1,000 asynchronous workers attempt to deploy a unit to the grid simultaneously, 
-- only the strongest survives the lock.
INSERT INTO units (callsign, spinal_catastrophism_level, tactical_grid_location) 
VALUES ('Node-0', 10, ST_SetSRID(ST_MakePoint(-97.1384, 49.8951), 4326))
ON CONFLICT (callsign) DO UPDATE 
SET spinal_catastrophism_level = units.spinal_catastrophism_level + 1;
```
