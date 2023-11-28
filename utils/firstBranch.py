def is_first_branch_newer(branch_a, branch_b):
    for token_a, token_b in zip(branch_a['tokens'], branch_b['tokens']):
        # Longer version always comes after shorter versions if they are equivalent up to that point
        if not token_b:
            return True

        if not token_a.isdigit():
            if not token_b.isdigit():
                # If both tokens are non-numeric, perform string comparison
                if token_b < token_a:
                    # 5.6-alpha comes before 5.6-beta
                    return True
                elif token_a == token_b:
                    # Equal, keep checking
                    continue
                return False
            else:
                # Numeric tokens are newer than non-numeric tokens
                # Example: 6.1-SNAPSHOT is older than 6.1.0
                return False
        else:
            # Numeric tokens are newer than non-numeric tokens
            # Example: 6.1-SNAPSHOT comes before 6.1.0
            if not token_b.isdigit():
                return True
            else:
                branch_a_int = int(token_a)
                branch_b_int = int(token_b)

                # Perform numeric comparison
                if branch_b_int < branch_a_int:
                    # Example: 5 comes before 6
                    return True
                elif branch_a_int == branch_b_int:
                    # Equal, keep checking
                    continue
                return False

    # Reaching this point means the branch_b version had all of the branch_a version's tokens and then some,
    # meaning the branch_b version is newer (later) than the branch_a version.
    return False
