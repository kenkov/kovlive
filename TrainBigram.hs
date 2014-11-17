module TrainBigram where

import Control.Applicative
import Control.Monad
--import Data.List
import qualified Data.Map.Strict as SM
import System.Environment (getArgs)
import System.IO  -- file I/O
import Text.Printf  -- printf

-- $setup
-- >>> import qualified Data.Map.Strict as SM

type Unigram = [String]
type Bigram = [(String, String)]
type Unicount = SM.Map String Double
type Bicount = SM.Map (String, String) Double
type Unimodel = SM.Map String Double
type Bimodel = SM.Map (String, String) Double

-- | train bigram model
-- >>> :{
--  train' ["<s>", "a", "b", "a", "b", "</s>"]
--         [("<s>", "a"), ("a", "b"), ("b", "a"), ("a", "b"), ("b", "</s>")] ==
--  (SM.fromList [("</s>", 1.0),
--                ("<s>", 1.0),
--                ("a", 2.0),
--                ("b", 2.0)],
--   SM.fromList [(("<s>", "a"), 1.0),
--                (("a","b"), 2.0),
--                (("b", "</s>"), 1.0),
--                (("b", "a"), 1.0)])
-- :}
-- True
--
train' :: Unigram -> Bigram -> (Unicount, Bicount)
train' uni bi =
    (count uni, count bi)
    where
        count :: (Ord a) => [a] -> SM.Map a Double
        count = foldl (\m x -> SM.insertWith (+) x 1 m) SM.empty


-- | train
-- >>> let unicount = SM.fromList [("</s>", 1.0), ("<s>", 1.0), ("a", 2.0), ("b", 2.0)]
-- >>> let bicount = SM.fromList [(("<s>", "a"), 1.0), (("a", "b"), 2.0), (("b", "</s>"), 1.0), (("b", "a"), 1.0)]
-- >>> :{
-- train unicount bicount ==
--  (SM.fromList [("</s>", 0.2),
--                ("a", 0.4),
--                ("b", 0.4)],
--   SM.fromList [(("<s>", "a"), 1.0),
--                (("a", "b"), 1.0),
--                (("b", "</s>"), 0.5),
--                (("b", "a"), 0.5)])
-- :}
-- True
train :: Unicount -> Bicount -> (Unimodel, Bimodel)
train unicount bicount =
    (
        SM.map (/ mapSum unicount') unicount'
        , SM.foldlWithKey (\a k@(w0, _) b -> case SM.lookup w0 unicount of
                Nothing -> a
                Just n -> SM.insert k (b / n) a)
            SM.empty bicount
    )
    where
        -- startSymbol は unimodel では数えない: P(<s>) == 1.0
        unicount' = SM.filterWithKey (\k _ -> k /= "<s>") unicount
        mapSum = SM.foldl (+) 0

trainBigram :: Unigram -> Bigram -> (Unimodel, Bimodel)
trainBigram unigram bigram = uncurry train $ train' unigram bigram

addSymbol :: [String] -> [String]
addSymbol xs = ["<s>"] ++ xs ++ ["</s>"]

main :: IO ()
main = do
    filename <- head <$> getArgs
    ifs <- openFile filename ReadMode
    xs <- map words . lines <$> hGetContents ifs
    let unigram = concat [addSymbol word |  word <- xs]
    let bigram = concat [zip word (tail word) | word <- [addSymbol word | word <- xs]]
    let (unimodel, bimodel) = trainBigram unigram bigram

    -- print unigram model
    forM_ (SM.assocs unimodel) $ \(k, v) ->
        printf "%s\t%.6f\n" k v

    -- print bigram model
    forM_ (SM.assocs bimodel) $ \((w0, w1), v) ->
        printf "%s %s\t%.6f\n" w0 w1 v
