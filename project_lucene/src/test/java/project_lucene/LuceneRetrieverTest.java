package project_lucene;

import java.io.IOException;

import org.apache.lucene.queryparser.classic.ParseException;
import org.junit.Test;

/**
 * LuceneRetrieverTest
 */
public class LuceneRetrieverTest {

    @Test
    public void testRetriever() {
        try {
            LuceneRetriever retriever = new LuceneRetriever();
            retriever.executeQuery("test queru", 1);
        } catch (ParseException | IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }
}