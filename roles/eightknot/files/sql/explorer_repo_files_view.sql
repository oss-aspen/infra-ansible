-- augur_data.explorer_repo_files source

CREATE MATERIALIZED VIEW augur_data.explorer_repo_files
TABLESPACE pg_default
AS SELECT rl.repo_id,
    r.repo_name,
    r.repo_path,
    rl.rl_analysis_date,
    rl.file_path,
    rl.file_name
   FROM augur_data.repo_labor rl
     JOIN augur_data.repo r ON rl.repo_id = r.repo_id
  WHERE ((rl.repo_id, rl.rl_analysis_date) IN ( SELECT DISTINCT ON (repo_labor.repo_id) repo_labor.repo_id,
            repo_labor.rl_analysis_date
           FROM augur_data.repo_labor
          ORDER BY repo_labor.repo_id, repo_labor.rl_analysis_date DESC))
WITH NO DATA;

-- View indexes:
CREATE INDEX idx_explorer_repo_files_repo_id ON augur_data.explorer_repo_files USING btree (repo_id);