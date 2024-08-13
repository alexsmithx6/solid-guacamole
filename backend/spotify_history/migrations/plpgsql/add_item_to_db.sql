CREATE OR REPLACE PROCEDURE public.add_item_to_db(IN item jsonb)
LANGUAGE 'plpgsql'  -- Use 'plpgsql' for procedural SQL, not 'sql'
AS $BODY$
DECLARE
    artist_obj jsonb;
BEGIN
	-- ARTIST
    -- Iterate over each artist in the JSONB array
    FOR artist_obj IN
        SELECT jsonb_array_elements(item->'track'->'artists') AS artist_obj
        UNION
        SELECT jsonb_array_elements(item->'track'->'album'->'artists') AS artist_obj
    LOOP
        -- Extract relevant fields from the artist JSON object
        INSERT INTO spotify_history_artist (id, name)
        VALUES (
			(artist_obj->>'id')::varchar, 
			(artist_obj->>'name')::varchar
		)
        ON CONFLICT (id) DO NOTHING; -- Optional: Prevents duplicates if id is unique
    END LOOP;

	-- ALBUM
	INSERT INTO spotify_history_album(id, name, release_date, len, art_url)
	VALUES (
		(item->'track'->'album'->>'id')::varchar, 
		(item->'track'->'album'->>'name')::varchar, 
		(item->'track'->'album'->>'release_date')::date,
		(item->'track'->'album'->'total_tracks')::int,
		(item->'track'->'album'->'images'->0->>'url')::varchar
	)
	ON CONFLICT (id) DO NOTHING; -- Optional: Prevents duplicates if id is unique

	-- SONG
	INSERT INTO spotify_history_song(id, album_id, name, index, duration)
	VALUES (
		(item->'track'->>'id')::varchar, 
		(item->'track'->'album'->>'id')::varchar, 
		(item->'track'->>'name')::varchar,
		(item->'track'->>'track_number')::int,
		(item->'track'->>'duration_ms')::int
	)
	ON CONFLICT (id) DO NOTHING; -- Optional: Prevents duplicates if id is unique

    -- Iterate over each artist in the JSONB array
    FOR artist_obj IN
        SELECT jsonb_array_elements(item->'track'->'album'->'artists') AS artist_obj
    LOOP
        -- ARTIST_ALBUM
        INSERT INTO spotify_history_artist_album(artist_id, album_id)
        VALUES (
			(artist_obj->>'id')::varchar, 
            (item->'track'->'album'->>'id')::varchar
        )
        ON CONFLICT (artist_id, album_id) DO NOTHING; -- Optional: Prevents duplicates if id is unique
    END LOOP;

    -- Iterate over each artist in the JSONB array
    FOR artist_obj IN
        SELECT jsonb_array_elements(item->'track'->'artists') AS artist_obj
    LOOP
        -- ARTIST_ALBUM
        INSERT INTO spotify_history_artist_song(artist_id, song_id)
        VALUES (
			(artist_obj->>'id')::varchar, 
            (item->'track'->>'id')::varchar
        )
        ON CONFLICT (artist_id, song_id) DO NOTHING; -- Optional: Prevents duplicates if id is unique
    END LOOP;

END;
$BODY$;
ALTER PROCEDURE public.add_item_to_db OWNER TO admin;
GRANT EXECUTE ON PROCEDURE public.add_item_to_db TO pg_write_all_data;
REVOKE ALL ON PROCEDURE public.add_item_to_db FROM PUBLIC;
COMMENT ON PROCEDURE public.add_item_to_db IS 'Deserialize item JSON and add selected metadata INTO database';
