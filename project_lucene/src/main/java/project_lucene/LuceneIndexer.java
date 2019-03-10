package project_lucene;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Properties;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * This is a class to generate a lucene index from a corpus. LuceneIndexer
 */
public class LuceneIndexer {

    private String PROPERTIES = "resources/config.properties";
    private String corpusPath;
    private String indexPath;
    private Boolean reindex;

    private IndexWriter writer;
    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private ArrayList<File> queue = new ArrayList<File>();

    /**
     * Constructor for the lucene indexer
     */
    public LuceneIndexer() {
        loadProperties();
        assert intializeIndex();
    }

    /**
     * Intialize the indexer based on the loaded configuration.
     */
    private boolean intializeIndex() {
        if (!this.reindex) {
            return true;
        }
        try {
            FSDirectory dir = FSDirectory.open(new File(indexPath));
            IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, analyzer);
            writer = new IndexWriter(dir, config);
            return true;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }

    }

    /**
     * Load in the properties for this indexer from the LuceneIndexer
     */
    private void loadProperties() {
        Properties prop = new Properties();
        try {
            InputStream input = new FileInputStream(PROPERTIES);
            prop.load(input);
            indexPath = prop.getProperty("INDEX_PATH");
            reindex = Boolean.valueOf(prop.getProperty("REINDEX"));
            corpusPath = prop.getProperty("CORPUS_PATH");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException ioException) {
            ioException.printStackTrace();
        }
    }

    public boolean create_index() {

        try {
            if(reindex) {
                indexFileOrDirectory(corpusPath);
            }
            return true;
        
        } catch (IOException e) {
            //TODO: handle exception
            return false;
        }
    }

    /**
     * Indexes a file or directory
     *
     * @param fileName the name of a text file or a folder we wish to add to the
     *                 index
     * @throws java.io.IOException when exception
     */
    private void indexFileOrDirectory(String fileName) throws IOException {
        // ===================================================
        // gets the list of files in a folder (if user has submitted
        // the name of a folder) or gets a single file name (is user
        // has submitted only the file name)
        // ===================================================
        addFiles(new File(fileName));

        int originalNumDocs = writer.numDocs();

        for (File f : queue) {
            FileReader fr = null;
            try {
                Document doc = new Document();

                // ===================================================
                // add contents of file
                // ===================================================
                fr = new FileReader(f);
                doc.add(new TextField("contents", fr));
                doc.add(new StringField("path", f.getPath(), Field.Store.YES));
                doc.add(new StringField("filename", f.getName(), Field.Store.YES));

                writer.addDocument(doc);
                System.out.println("Added: " + f);
            } catch (Exception e) {
                System.out.println("Could not add: " + f);
            } finally {
                fr.close();
            }
        }

        int newNumDocs = writer.numDocs();
        System.out.println("");
        System.out.println("************************");
        System.out.println((newNumDocs - originalNumDocs) + " documents added.");
        System.out.println("************************");

        queue.clear();
        closeIndex();
    }

    private void closeIndex() throws IOException{
        writer.close();
    }

    private void addFiles(File file) {

        if (!file.exists()) {
            System.out.println(file + " does not exist.");
        }
        if (file.isDirectory()) {
            for (File f : file.listFiles()) {
                addFiles(f);
            }
        } else {
            String filename = file.getName().toLowerCase();
            // ===================================================
            // Only index text files
            // ===================================================
            if (filename.endsWith(".htm") || filename.endsWith(".html") || filename.endsWith(".xml")
                    || filename.endsWith(".txt")) {
                queue.add(file);
            } else {
                System.out.println("Skipped " + filename);
            }
        }
    }
}