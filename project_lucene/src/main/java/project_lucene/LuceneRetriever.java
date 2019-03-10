package project_lucene;

import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import java.io.File;
import java.io.FileInputStream;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * LuceneRetriever
 */
public class LuceneRetriever {
    private IndexReader reader;
    private IndexSearcher searcher;
    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);

    private String indexPath;
    private String outputPath;
    private String PROPERTIES = "resources/config.properties";

    public LuceneRetriever() {
        loadProperties();
        try {
            IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
            indexPath)));
            searcher = new IndexSearcher(reader);       
        } catch (Exception e) {
            e.printStackTrace();
        }
        
    }

    public TopScoreDocCollector executeQuery(String query, int queryNumber) throws ParseException, IOException {
        TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
        Query q = new QueryParser(Version.LUCENE_47, "contents",
            analyzer).parse(query);
        searcher.search(q, collector);
        ScoreDoc[] hits = collector.topDocs().scoreDocs;
        String outputFileName = outputPath+ "/Lucene_"+ Integer.toString(queryNumber)+".txt";
        try (FileWriter fw = new FileWriter(outputFileName)) {
            System.out.println("Found " + hits.length + " hits.");
            for (int i = 0; i < hits.length; ++i) {
              int docId = hits[i].doc;
              Document d = searcher.doc(docId);
              //query_id Q0 doc_id rank LuceneStandard system_name
                String docName = d.get("path");
                docName = docName.substring(docName.lastIndexOf('/') + 1);
                query = query.replace(" ", "_");
                docName = docName.replace(".html", "");
              String docString = query + " Q0 " + docName +" " + (i + 1) + " " +
                  hits[i].score +" Lucene\n";
              fw.append(docString);
              System.out.println((i + 1) + ". " + docName
                  + " score=" + hits[i].score);
            }
        }


        return collector;
    }
    private void loadProperties() {
        Properties prop = new Properties();
        try {
            InputStream input = new FileInputStream(PROPERTIES);
            prop.load(input);
            indexPath = prop.getProperty("INDEX_PATH");
            outputPath = prop.getProperty("OUTPUT_PATH");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException ioException) {
            ioException.printStackTrace();
        }
    }


    
}