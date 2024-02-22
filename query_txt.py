query_txt = """
        query PickABrickQuery($input: ElementQueryArgs, $sku: String) {
          __typename
          elements(input: $input) {
            count
            facets {
              ...FacetData
              __typename
            }
            sortOptions {
              ...Sort_SortOptions
              __typename
            }
            results {
              ...ElementLeafData
              __typename
            }
            set {
              id
              type
              name
              imageUrl
              instructionsUrl
              pieces
              inStock
              price {
                formattedAmount
                __typename
              }
              __typename
            }
            total
            __typename
          }
        }

        fragment FacetData on Facet {
          id
          key
          name
          labels {
            count
            key
            name
            children {
              count
              key
              name
              ... on FacetValue {
                value
                __typename
              }
              __typename
            }
            ... on FacetValue {
              value
              __typename
            }
            ... on FacetRange {
              from
              to
              __typename
            }
            __typename
          }
          __typename
        }

        fragment Sort_SortOptions on SortOptions {
          id
          key
          direction
          label
          analyticLabel
          __typename
        }

        fragment ElementLeafData on Element {
          id
          name
          categories {
            name
            key
            __typename
          }
          inStock
          ... on SingleVariantElement {
            variant {
              ...ElementLeafVariant
              __typename
            }
            __typename
          }
          ... on MultiVariantElement {
            variants {
              ...ElementLeafVariant
              __typename
            }
            __typename
          }
          __typename
        }

        fragment ElementLeafVariant on ElementVariant {
          id
          price {
            centAmount
            formattedAmount
            __typename
          }
          attributes {
            designNumber
            colourId
            deliveryChannel
            maxOrderQuantity
            system
            quantityInSet(sku: $sku)
            indexImageURL
            __typename
          }
          __typename
        }
        """