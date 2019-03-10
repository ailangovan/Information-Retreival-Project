package project_lucene;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.nodes.TextNode;
import org.jsoup.select.Elements;

/**
 * Hello world!
 *
 */
public class Lucene 
{
    private static String PATH_NAME;
    private static String PROPERTIES = "resources/config.properties";
    public static void main ( String[] args )
    {
        LuceneIndexer indexer = new LuceneIndexer();;
        LuceneRetriever retriever = new LuceneRetriever();
        loadProperties();
        try {
            Document doc = Jsoup.parse(new File(PATH_NAME), "UTF-8");
            Elements queries = doc.select("DOC");
            for(Element e : queries){
                TextNode node = (TextNode) e.childNode(2);
                Element docId = e.getElementsByTag("docno").get(0);
                TextNode docNo = (TextNode) docId.childNode(0);
                System.out.println(docNo);
                System.out.println(node);

                String query = node.toString();
                int queryNo = Integer.valueOf(docNo.toString().trim());
                try{
                    retriever.executeQuery(QueryParser.escape(query), queryNo);
                } catch (ParseException e2) {
                    System.out.println("ERROR @ Query#" + docNo);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        

        System.out.println( "Hello World!" );
    }

    private static void loadProperties() {
        Properties prop = new Properties();
        try {
            InputStream input = new FileInputStream(PROPERTIES);
            prop.load(input);
            PATH_NAME = prop.getProperty("QUERY_PATH");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException ioException) {
            ioException.printStackTrace();
        }
    }
}
