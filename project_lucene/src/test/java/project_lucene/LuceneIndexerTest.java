package project_lucene;

import static org.junit.Assert.assertTrue;

import org.junit.Test;

/**
 * LuceneIndexer
 */
public class LuceneIndexerTest {

    @Test
    public void testInitialization(){
        LuceneIndexer index = new LuceneIndexer();
        assertTrue( true );
    }

    @Test
    public void testIndexer() {
        LuceneIndexer index = new LuceneIndexer();
        assertTrue("Did the indexer generate an index?", index.create_index());
    }
}